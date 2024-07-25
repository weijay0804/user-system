"""Add user_tokens table updated_at col

Revision ID: 9bc22ba4dc43
Revises: 851bfbcfcdcf
Create Date: 2024-06-21 19:25:15.213484

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9bc22ba4dc43'
down_revision: Union[str, None] = '851bfbcfcdcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_tokens', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_tokens', 'updated_at')
    # ### end Alembic commands ###