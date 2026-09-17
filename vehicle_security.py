import time
import math


# =========================================================
# PC / WSL SIMULATION
# =========================================================

print("======================================")
print(" PC / WSL SIMULATION MODE")
print("======================================")
print()


# =========================================================
# SIMULATED GPIO
# =========================================================

class FakeSensor:
    def __init__(self):
        # False = object detected
        self.value = False

    def deinit(self):
        pass


class FakeOutput:
    def __init__(self):
        self.value = False

    def deinit(self):
        pass


ir_sensor = FakeSensor()
relay = FakeOutput()
buzzer = FakeOutput()

print("GPIO simulation enabled")


# =========================================================
# SIMULATED ADXL345
# =========================================================

class FakeAccelerometer:

    def __init__(self):
        # Normal vehicle acceleration
        self.acceleration = (0.0, 0.0, 9.8)


accelerometer = FakeAccelerometer()

print("ADXL345 simulation enabled")


# =========================================================
# SIMULATED FINGERPRINT
# =========================================================

fingerprint_available = True


# =========================================================
# SIMULATED GPS
# =========================================================

gps_available = True

# Example location
SIMULATED_LATITUDE = 12.9716
SIMULATED_LONGITUDE = 77.5946


# =========================================================
# SIMULATED GSM
# =========================================================

gsm_available = True

PHONE_NUMBER = "+91XXXXXXXXXX"


# =========================================================
# BUZZER FUNCTIONS
# =========================================================

def buzzer_on():

    buzzer.value = True

    print("Buzzer ON")


def buzzer_off():

    buzzer.value = False

    print("Buzzer OFF")


def alarm():

    print("Alarm activated")

    for i in range(5):

        buzzer_on()

        time.sleep(0.2)

        buzzer_off()

        time.sleep(0.2)


# =========================================================
# RELAY FUNCTIONS
# =========================================================

def vehicle_unlock():

    print("Vehicle unlocked")

    relay.value = True


def vehicle_lock():

    print("Vehicle locked")

    relay.value = False


# =========================================================
# FINGERPRINT FUNCTIONS
# =========================================================

def fingerprint_check():

    if not fingerprint_available:

        print("Fingerprint sensor unavailable")

        return False


    print("Fingerprint sensor simulation enabled")

    print("Waiting for fingerprint...")

    time.sleep(2)

    print("Finger detected")

    print("--------------------------------")
    print("Fingerprint MATCHED")
    print("ID: 1")
    print("Confidence: 100")
    print("--------------------------------")

    return True


# =========================================================
# GPS FUNCTIONS
# =========================================================

def get_gps_location():

    if not gps_available:

        return None, None


    print("Getting GPS location...")

    time.sleep(1)

    latitude = SIMULATED_LATITUDE
    longitude = SIMULATED_LONGITUDE

    print("GPS location obtained")

    print("Latitude:", latitude)
    print("Longitude:", longitude)

    return latitude, longitude


# =========================================================
# GSM SMS FUNCTION
# =========================================================

def send_sms(message):

    if not gsm_available:

        print("GSM module unavailable")

        return


    print()
    print("======================================")
    print(" SIMULATED SMS")
    print("======================================")

    print("To:", PHONE_NUMBER)

    print("Message:")
    print(message)

    print("======================================")
    print("SMS sent successfully (SIMULATION)")
    print("======================================")
    print()


# =========================================================
# ACCIDENT DETECTION
# =========================================================

ACCIDENT_THRESHOLD = 3.0


def check_accident():

    try:

        x, y, z = accelerometer.acceleration

        magnitude = math.sqrt(
            x * x +
            y * y +
            z * z
        )


        print(
            "Acceleration:"
            " X={:.2f}"
            " Y={:.2f}"
            " Z={:.2f}"
            " Magnitude={:.2f}".format(
                x,
                y,
                z,
                magnitude
            )
        )


        # Detect abnormal acceleration

        if magnitude > ACCIDENT_THRESHOLD * 9.81:

            print("!!!!!!!!!!!!!!!!!!!!!!!!")
            print("ACCIDENT DETECTED")
            print("!!!!!!!!!!!!!!!!!!!!!!!!")

            return True


    except Exception as e:

        print("ADXL345 error:", e)


    return False


# =========================================================
# ACCIDENT ALERT
# =========================================================

def accident_alert():

    print("Starting accident alert")

    alarm()


    latitude, longitude = get_gps_location()


    if latitude is not None and longitude is not None:

        location = (
            "Latitude: {:.6f}\n"
            "Longitude: {:.6f}\n"
            "Google Maps: "
            "https://maps.google.com/?q={:.6f},{:.6f}"
        ).format(
            latitude,
            longitude,
            latitude,
            longitude
        )

    else:

        location = "GPS location unavailable"


    message = (
        "EMERGENCY ALERT!\n"
        "Possible vehicle accident detected.\n\n"
        "{}"
    ).format(location)


    print(message)

    send_sms(message)


# =========================================================
# UNAUTHORIZED ACCESS ALERT
# =========================================================

def unauthorized_alert():

    print("UNAUTHORIZED ACCESS DETECTED")

    alarm()


    latitude, longitude = get_gps_location()


    if latitude is not None and longitude is not None:

        location = (
            "\nLocation:\n"
            "https://maps.google.com/?q={:.6f},{:.6f}"
        ).format(
            latitude,
            longitude
        )

    else:

        location = "\nGPS location unavailable"


    message = (
        "SECURITY ALERT!\n"
        "Unauthorized fingerprint detected."
        "{}"
    ).format(location)


    send_sms(message)


# =========================================================
# IR SENSOR
# =========================================================

def check_ir_sensor():

    # False means object detected
    # This is the same logic as the original project

    if ir_sensor.value is False:

        print("IR sensor: Object detected")

        return True


    return False


# =========================================================
# MAIN SECURITY SYSTEM
# =========================================================

def main():

    print()
    print("======================================")
    print(" MULTIFUNCTIONAL VEHICLE SECURITY")
    print("======================================")
    print()


    vehicle_lock()


    # -----------------------------------------------------
    # DRIVER AUTHENTICATION
    # -----------------------------------------------------

    print("Driver authentication required.")

    authenticated = fingerprint_check()


    if authenticated:

        print()
        print("DRIVER AUTHENTICATED")
        print("Vehicle starting...")
        print()


        vehicle_unlock()

        time.sleep(2)


        # -------------------------------------------------
        # PC SIMULATION
        # -------------------------------------------------

        print()
        print("Vehicle monitoring started")
        print()


        # Run only a few times for PC testing
        # instead of an infinite loop

        for i in range(5):

            print("--------------------------------------")
            print("Monitoring cycle:", i + 1)
            print("--------------------------------------")


            # ---------------------------------------------
            # ACCIDENT DETECTION
            # ---------------------------------------------

            if check_accident():

                vehicle_lock()

                accident_alert()

                print("Accident alert completed.")

                break


            # ---------------------------------------------
            # IR SENSOR
            # ---------------------------------------------

            if check_ir_sensor():

                print("IR event detected")


            time.sleep(1)


    else:

        print()
        print("ACCESS DENIED")
        print("Vehicle remains locked.")
        print()


        vehicle_lock()

        unauthorized_alert()


# =========================================================
# PROGRAM START
# =========================================================

try:

    main()


except KeyboardInterrupt:

    print()
    print("Program stopped by user")


finally:

    vehicle_lock()

    buzzer_off()

    ir_sensor.deinit()
    relay.deinit()
    buzzer.deinit()

    print("GPIO cleanup completed")

