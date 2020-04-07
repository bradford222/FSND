"""empty message

Revision ID: b0dc77800bc6
Revises: da319f69c398
Create Date: 2020-04-06 14:51:43.216824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0dc77800bc6'
down_revision = 'da319f69c398'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('alter table "Artist" alter genres type varchar[] using array[genres];')
    op.execute('alter table "Venue" alter genres type varchar[] using array[genres];')
    
def downgrade():
    op.execute('alter table "Artist" alter genres type varchar;')
    op.execute('alter table "Venue" alter genres type varchar;')
