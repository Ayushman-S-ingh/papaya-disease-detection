from tensorflow.keras.models import load_model
from tensorflow.keras.layers import BatchNormalization


# =====================================================
# CUSTOM BATCH NORMALIZATION
# =====================================================
class CustomBatchNormalization(BatchNormalization):
    def __init__(self, *args, **kwargs):

        kwargs.pop("renorm", None)
        kwargs.pop("renorm_clipping", None)
        kwargs.pop("renorm_momentum", None)
        kwargs.pop("synchronized", None)

        super().__init__(*args, **kwargs)


# =====================================================
# LOAD OLD MODEL
# =====================================================
model = load_model(
    "app/ml/papaya_model.h5",
    custom_objects={
        "CustomBatchNormalization": CustomBatchNormalization,
        "BatchNormalization": CustomBatchNormalization,
    },
    compile=False
)


# =====================================================
# SAVE NEW KERAS MODEL
# =====================================================
model.save("app/ml/papaya_model.keras")

print("✅ Model converted successfully!")