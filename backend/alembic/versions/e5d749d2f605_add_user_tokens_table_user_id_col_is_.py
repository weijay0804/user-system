"""Add user_tokens table user_id col is unique

Revision ID: e5d749d2f605
Revises: 9bc22ba4dc43
Create Date: 2024-06-21 19:36:13.963336

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e5d749d2f605'
down_revision: Union[str, None] = '9bc22ba4dc43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user_tokens', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_tokens', type_='unique')
    # ### end Alembic commands ###