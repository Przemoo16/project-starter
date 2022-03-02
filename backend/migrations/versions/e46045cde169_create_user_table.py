"""Create user table

Revision ID: e46045cde169
Revises: 
Create Date: 2022-02-26 17:19:09.542807

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'e46045cde169'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('confirmed_email', sa.Boolean(), nullable=True),
    sa.Column('confirmation_email_key', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('reset_password_key', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_confirmation_email_key'), 'user', ['confirmation_email_key'], unique=True)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_reset_password_key'), 'user', ['reset_password_key'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_reset_password_key'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_confirmation_email_key'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###