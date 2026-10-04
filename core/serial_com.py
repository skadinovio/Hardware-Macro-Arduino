import serial
import serial.tools.list_ports

class SerialManager:
    def __init__(self):
        self.serial_conn = None

    def connect(self, port, baudrate=9600):
        try:
            self.serial_conn = serial.Serial(port, baudrate, timeout=1)
            print(f"Terhubung ke {port}")
            return True
        except Exception as e:
            print(f"Gagal koneksi: {e}")
            return False

    def send_command(self, command):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.write(f"{command}\n".encode())
            print(f"-> Serial Send: {command}")
        else:
            # Simulasi print jika Arduino belum dicolok (untuk testing GUI)
            print(f"[Simulasi Arduino] -> {command}")
            
    def get_available_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]