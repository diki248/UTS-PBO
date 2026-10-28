import json
from abc import ABC, abstractmethod

# RULE BONUS: persentase ini merupakan asumsi contoh,
# karena soal tidak mencantumkan persentase bonus.
BONUS_RULES = {
    "PERF2026": 0.05,
    "SENIOR10": 0.10,
    "LEAD2026": 0.15
}


def rupiah(angka):
    return "Rp" + f"{angka:,.0f}".replace(",", ".")


# ==================== EMPLOYEE ====================

class Employee(ABC):
    def __init__(self, emp_id, name, base_salary, bonus_code):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = float(base_salary)
        self.bonus_code = bonus_code

    def calculate_bonus(self):
        persen = BONUS_RULES.get(self.bonus_code, 0)
        return self.base_salary * persen

    @abstractmethod
    def calculate_salary(self):
        pass

    def display_info(self):
        print(f"ID Karyawan : {self.emp_id}")
        print(f"Nama        : {self.name}")
        print(f"Gaji Pokok  : {rupiah(self.base_salary)}")
        print(f"Kode Bonus  : {self.bonus_code or '-'}")
        print(f"Bonus       : {rupiah(self.calculate_bonus())}")
        print(f"Total Gaji  : {rupiah(self.calculate_salary())}")
        print("-" * 50)


class PermanentEmployee(Employee):
    # OVERRIDE: gaji tetap = gaji pokok + bonus
    def calculate_salary(self):
        return self.base_salary + self.calculate_bonus()


class ContractEmployee(Employee):
    # OVERRIDE: asumsi karyawan kontrak menerima gaji pokok saja
    def calculate_salary(self):
        return self.base_salary


# ==================== SENSOR ====================

class Sensor(ABC):
    def __init__(self, sensor_id, location, temperature,
                 original_status, operator_id):
        self.sensor_id = sensor_id
        self.location = location
        self.temperature = float(temperature)
        self.original_status = original_status
        self.operator_id = operator_id

    @abstractmethod
    def determine_status(self):
        pass

    def display_info(self):
        status = self.determine_status()
        print(f"ID Sensor    : {self.sensor_id}")
        print(f"Lokasi       : {self.location}")
        print(f"Suhu         : {self.temperature:.1f} C")
        print(f"Status JSON  : {self.original_status}")
        print(f"Status Hasil : {status}")
        print("Operator     : " +
              (str(self.operator_id) if self.operator_id is not None
               else "Belum ditetapkan"))
        if status != self.original_status:
            print("Peringatan   : Status hasil berbeda dari JSON")
        print("-" * 50)


class TemperatureSensor(Sensor):
    # OVERRIDE: batas suhu adalah asumsi contoh, bukan aturan eksplisit soal.
    def determine_status(self):
        if self.temperature < 60:
            return "NORMAL"
        elif self.temperature < 80:
            return "WARNING"
        return "DANGER"


# ==================== MEMBACA JSON ====================

def load_employees(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    employees = []
    for item in data["employees"]:
        if item["is_permanent"]:
            obj = PermanentEmployee(
                item["emp_id"], item["name"],
                item["base_salary"], item["bonus_code"]
            )
        else:
            obj = ContractEmployee(
                item["emp_id"], item["name"],
                item["base_salary"], item["bonus_code"]
            )
        employees.append(obj)
    return employees


def load_sensors(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    sensors = []
    for item in data["readings"]:
        sensors.append(TemperatureSensor(
            item["sensor_id"], item["location"],
            item["temperature"], item["status"],
            item["operator_id"]
        ))
    return sensors


# ==================== PROGRAM UTAMA ====================

def main():
    employees = load_employees("employee.json")
    sensors = load_sensors("sensor_logs.json")

    print("\\n" + "=" * 50)
    print("LAPORAN DATA KARYAWAN")
    print("=" * 50)
    for employee in employees:
        # POLYMORPHISM: metode sama, hasil sesuai jenis objek.
        employee.display_info()

    total_gaji = sum(e.calculate_salary() for e in employees)
    total_bonus = sum(e.calculate_bonus() for e in employees)
    tetap = sum(isinstance(e, PermanentEmployee) for e in employees)
    kontrak = len(employees) - tetap

    print("\\nRINGKASAN KARYAWAN")
    print(f"Jumlah karyawan : {len(employees)}")
    print(f"Karyawan tetap  : {tetap}")
    print(f"Karyawan kontrak: {kontrak}")
    print(f"Total bonus     : {rupiah(total_bonus)}")
    print(f"Total gaji      : {rupiah(total_gaji)}")

    print("\\n" + "=" * 50)
    print("LAPORAN SENSOR SUHU")
    print("=" * 50)
    for sensor in sensors:
        sensor.display_info()

    jumlah_status = {"NORMAL": 0, "WARNING": 0, "DANGER": 0}
    tanpa_operator = 0
    for sensor in sensors:
        jumlah_status[sensor.determine_status()] += 1
        if sensor.operator_id is None:
            tanpa_operator += 1

    print("\\nRINGKASAN SENSOR")
    print(f"Jumlah sensor      : {len(sensors)}")
    print(f"Status NORMAL      : {jumlah_status['NORMAL']}")
    print(f"Status WARNING     : {jumlah_status['WARNING']}")
    print(f"Status DANGER      : {jumlah_status['DANGER']}")
    print(f"Belum ada operator : {tanpa_operator}")


if __name__ == "__main__":
    main()
