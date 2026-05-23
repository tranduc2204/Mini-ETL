# Để đảm bảo:

# transform đúng
# schema đúng
# không mất data
# CDC merge đúng
# pipeline không bị regression
import pandas as pd

from scripts.silver.silver_orders import silver_orders


# def test_delete_removed():

#     df = pd.DataFrame([
#         {
#             "order_id": 1,
#             "operation_type": "DELETE"
#         }
#     ])

#     result = silver_orders(df)

#     assert result.empty



