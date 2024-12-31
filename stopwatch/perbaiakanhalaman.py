import streamlit as st
import time
from datetime import datetime, timedelta
import winsound

class TimeApp:
    def __init__(self):
        self.init_session_state()

    def init_session_state(self):
        if "sw_start_time" not in st.session_state:
            st.session_state.sw_start_time = None
        if "sw_elapsed_time" not in st.session_state:
            st.session_state.sw_elapsed_time = 0
        if "sw_running" not in st.session_state:
            st.session_state.sw_running = False
        if "timer_running" not in st.session_state:
            st.session_state.timer_running = False
        if "timer_end_time" not in st.session_state:
            st.session_state.timer_end_time = None

    @staticmethod
    def format_time(seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes):02}:{int(seconds):02}"

    @staticmethod
    def set_background(color):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-color: {color};
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def set_sidebar_background(image_url):
        st.markdown(
            f"""
            <style>
            [data-testid="stSidebar"] {{
                background-image: url({image_url});
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def set_home_background(image_url):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url({image_url});
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    def stopwatch(self):
        self.set_background("#ADD8E6")
        st.title("Stopwatch")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Start Stopwatch"):
                if not st.session_state.sw_running:
                    st.session_state.sw_start_time = time.time() - st.session_state.sw_elapsed_time
                    st.session_state.sw_running = True
        with col2:
            if st.button("Stop Stopwatch"):
                if st.session_state.sw_running:
                    st.session_state.sw_elapsed_time = time.time() - st.session_state.sw_start_time
                    st.session_state.sw_running = False
        with col3:
            if st.button("Reset Stopwatch"):
                st.session_state.sw_start_time = None
                st.session_state.sw_elapsed_time = 0
                st.session_state.sw_running = False

        timer_placeholder = st.empty()
        while st.session_state.sw_running:
            st.session_state.sw_elapsed_time = time.time() - st.session_state.sw_start_time
            timer_placeholder.subheader(f"{self.format_time(st.session_state.sw_elapsed_time)}")
            time.sleep(0.1)

        timer_placeholder.subheader(f"mulai: {self.format_time(st.session_state.sw_elapsed_time)}")

    def timer(self):
        self.set_background("#FF7276")
        st.title("Timer")

        minutes = st.number_input("Set Timer (Minutes):", min_value=0, max_value=60, value=1)
        if st.button("Start Timer"):
            st.session_state.timer_end_time = time.time() + minutes * 60
            st.session_state.timer_running = True

        timer_placeholder = st.empty()
        while st.session_state.timer_running:
            remaining_time = st.session_state.timer_end_time - time.time()
            if remaining_time <= 0:
                st.session_state.timer_running = False
                timer_placeholder.subheader("Time's Up!")
                break
            timer_placeholder.subheader(f"Remaining Time: {self.format_time(remaining_time)}")
            time.sleep(0.1)

    def digital_clock(self):
        self.set_background("#90EE90")
        st.title("Digital Clock")

        st.markdown(
            """
            <style>
            .clock-style {
                font-size: 50px;
                font-weight: bold;
                color: #FF4500; /* Orangered */
                text-align: center;
                margin-top: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        time_placeholder = st.empty()
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            time_placeholder.markdown(f"<div class='clock-style'>{current_time}</div>", unsafe_allow_html=True)
            time.sleep(1)

    def alarm(self):
        self.set_background("#FFD700")
        st.title("Alarm Waktu")

        waktu_alarm = st.text_input("Masukkan waktu alarm yang kamu inginkan:", value="00:00:00")
        aktifkan_alarm = st.button("Aktifkan Alarm")

        if aktifkan_alarm:
            st.success("Alarm diatur pada: " + waktu_alarm)

            def mainkan_alarm():
                for _ in range(5):
                    winsound.Beep(2500, 1000)

            while True:
                waktu_sekarang = datetime.now().strftime("%H:%M:%S")
                if waktu_sekarang == waktu_alarm:
                    st.balloons()
                    st.success("Waktu alarm selesai!")
                    mainkan_alarm()
                    break
                time.sleep(1)

    def home(self):
        self.set_home_background("https://png.pngtree.com/thumb_back/fh260/background/20240102/pngtree-hd-texture-background-with-vintage-golden-wall-clock-image_13865592.png")
        st.title("Selamat Datang di Aplikasi Multifungsi")
        st.write("\nAplikasi ini menyediakan berbagai fitur waktu, seperti:")
        st.write("- Stopwatch")
        st.write("- Timer")
        st.write("- Jam Digital")
        st.write("- Alarm")
        st.write("\nGunakan sidebar untuk menavigasi ke fitur yang Anda butuhkan.")


# Main App
app = TimeApp()
app.set_sidebar_background("https://www.shutterstock.com/image-photo/wall-clock-showing-1000-2200-260nw-2498993337.jpg")
st.sidebar.title("Navigasi")
selected_feature = st.sidebar.radio(
    "Pilih fitur:", ("Home", "Stopwatch", "Timer", "Jam Digital", "Alarm")
)

if selected_feature == "Home":
    app.home()
elif selected_feature == "Stopwatch":
    app.stopwatch()
elif selected_feature == "Timer":
    app.timer()
elif selected_feature == "Jam Digital":
    app.digital_clock()
elif selected_feature == "Alarm":
    app.alarm()
