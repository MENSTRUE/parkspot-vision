from pathlib import Path

import streamlit as st
from PIL import Image

from src.predict import predict_image


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "parkspot_yolo11n_best.pt"
)


st.set_page_config(
    page_title="ParkSpot Vision",
    page_icon="🚗",
    layout="wide",
)


st.title(
    "🚗 ParkSpot Vision"
)

st.caption(
    "AI-assisted parking occupancy "
    "screening from fixed-camera images."
)


st.markdown(
    """
ParkSpot Vision mendeteksi area parkir
yang **kosong** dan **terisi** dari sebuah
gambar kamera parkir.

**AI memberikan estimasi okupansi.**
Hasil tetap perlu diverifikasi untuk
penggunaan operasional.
"""
)


if not MODEL_PATH.exists():

    st.error(
        "Model belum ditemukan di "
        "`models/parkspot_yolo11n_best.pt`"
    )

    st.stop()


confidence = st.sidebar.slider(
    "Detection confidence",
    min_value=0.10,
    max_value=0.90,
    value=0.25,
    step=0.05,
)


uploaded_file = st.file_uploader(
    "Upload gambar area parkir",
    type=[
        "jpg",
        "jpeg",
        "png",
    ],
)


if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert(
        "RGB"
    )

    st.subheader(
        "Input"
    )

    st.image(
        image,
        use_container_width=True,
    )


    with st.spinner(
        "Menganalisis slot parkir..."
    ):

        result = predict_image(
            image=image,
            model_path=MODEL_PATH,
            confidence=confidence,
        )


    st.divider()

    st.subheader(
        "Detection Result"
    )

    st.image(
        result[
            "annotated_image"
        ],
        use_container_width=True,
    )


    col1, col2, col3, col4 = (
        st.columns(4)
    )


    with col1:

        st.metric(
            "Total Detected Slots",
            result["total"],
        )


    with col2:

        st.metric(
            "Vacant",
            result["vacant"],
        )


    with col3:

        st.metric(
            "Occupied",
            result["occupied"],
        )


    with col4:

        st.metric(
            "Occupancy Rate",
            f"{result['occupancy_rate']:.1%}",
        )


    if result["total"] == 0:

        st.warning(
            "Tidak ada slot parkir yang "
            "terdeteksi pada gambar ini."
        )

    elif result["vacant"] > 0:

        st.success(
            f"✅ Diperkirakan tersedia "
            f"{result['vacant']} slot kosong."
        )

    else:

        st.error(
            "🚫 Tidak ada slot kosong "
            "yang terdeteksi."
        )


    with st.expander(
        "Lihat detail deteksi"
    ):

        if result["detections"]:

            st.dataframe(
                result[
                    "detections"
                ],
                use_container_width=True,
            )

        else:

            st.info(
                "Tidak ada deteksi."
            )


    st.info(
        "Jumlah slot adalah hasil deteksi model "
        "pada frame ini. Confidence dan occupancy "
        "hasil model bukan status operasional yang "
        "sudah diverifikasi."
    )