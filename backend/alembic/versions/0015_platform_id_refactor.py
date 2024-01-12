"""empty message

Revision ID: 0015_platform_id_refactor
Revises: 0014_asset_files
Create Date: 2024-01-12 02:08:14.962703

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0015_platform_id_refactor'
down_revision = '0014_asset_files'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    # Drop platform_slug foreign key on all tables
    with op.batch_alter_table('states', schema=None) as batch_op:
        batch_op.drop_constraint("states_ibfk_1", type_='foreignkey')
        batch_op.drop_column('platform_slug')

    with op.batch_alter_table('screenshots', schema=None) as batch_op:
        batch_op.drop_constraint("screenshots_ibfk_1", type_='foreignkey')
        batch_op.drop_column('platform_slug')

    with op.batch_alter_table('saves', schema=None) as batch_op:
        batch_op.drop_constraint("saves_ibfk_1", type_='foreignkey')
        batch_op.drop_column('platform_slug')

    with op.batch_alter_table('roms', schema=None) as batch_op:
        batch_op.drop_constraint("fk_platform_roms", type_='foreignkey')
    # Drop platform_slug foreign key on all tables

    # Change platforms primary key
    with op.batch_alter_table('platforms', schema=None) as batch_op:
        batch_op.drop_constraint(constraint_name="PRIMARY", type_="primary")
        batch_op.drop_column('n_roms')

    with op.batch_alter_table('platforms', schema=None) as batch_op:
        batch_op.execute("ALTER TABLE platforms ADD COLUMN id INTEGER(11) NOT NULL AUTO_INCREMENT PRIMARY KEY")
    # Change platforms primary key


    # Create platform id foreign key
    with op.batch_alter_table('states', schema=None) as batch_op:
        batch_op.add_column(sa.Column('platform_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))

    with op.batch_alter_table('states', schema=None) as batch_op:
        batch_op.create_foreign_key('states_platforms_FK', 'platforms', ['platform_id'], ['id'])

    with op.batch_alter_table('screenshots', schema=None) as batch_op:
        batch_op.add_column(sa.Column('platform_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))

    with op.batch_alter_table('screenshots', schema=None) as batch_op:
        batch_op.create_foreign_key('screenshots_platforms_FK', 'platforms', ['platform_id'], ['id'])

    with op.batch_alter_table('saves', schema=None) as batch_op:
        batch_op.add_column(sa.Column('platform_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))

    with op.batch_alter_table('saves', schema=None) as batch_op:
        batch_op.create_foreign_key('saves_platforms_FK', 'platforms', ['platform_id'], ['id'])

    with op.batch_alter_table('roms', schema=None) as batch_op:
        batch_op.add_column(sa.Column('platform_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))

    with op.batch_alter_table('roms', schema=None) as batch_op:
        batch_op.execute("update roms inner join platforms on roms.platform_slug = platforms.slug set roms.platform_id = platforms.id")
    
    # Update platform id values on other tables
    with op.batch_alter_table('roms', schema=None) as batch_op:    
        batch_op.create_foreign_key('roms_platforms_FK', 'platforms', ['platform_id'], ['id'])
        batch_op.drop_column('platform_slug')
    # Update platform id values on other tables
        
    # Create platform id foreign key


    # Clean roms table
    with op.batch_alter_table('roms', schema=None) as batch_op:
        batch_op.drop_column('p_sgdb_id')
        batch_op.drop_column('p_igdb_id')
        batch_op.drop_column('p_name')
    # Clean roms table
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('platforms', schema=None) as batch_op:
        batch_op.drop_column('id')

    with op.batch_alter_table('roms', schema=None) as batch_op:
        batch_op.add_column(sa.Column('platform_slug', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('p_name', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('p_igdb_id', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('p_sgdb_id', sa.String(length=10), nullable=True))
        batch_op.drop_constraint('roms_platforms_FK', type_='foreignkey')
        batch_op.create_foreign_key(None, 'platforms', ['platform_slug'], ['slug'])
        batch_op.drop_column('platform_id')

    with op.batch_alter_table('saves', schema=None) as batch_op:
        batch_op.add_column(sa.Column('platform_slug', sa.String(length=50), nullable=False))
        batch_op.create_foreign_key(None, 'platforms', ['platform_slug'], ['slug'], ondelete='CASCADE')

    with op.batch_alter_table('screenshots', schema=None) as batch_op:
        batch_op.add_column(sa.Column('platform_slug', sa.String(length=50), nullable=True))
        batch_op.create_foreign_key(None, 'platforms', ['platform_slug'], ['slug'], ondelete='CASCADE')

    with op.batch_alter_table('states', schema=None) as batch_op:
        batch_op.add_column(sa.Column('platform_slug', sa.String(length=50), nullable=False))
        batch_op.create_foreign_key(None, 'platforms', ['platform_slug'], ['slug'], ondelete='CASCADE')
    # ### end Alembic commands ###
