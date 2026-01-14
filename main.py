from datetime import datetime

class Patient:
    def __init__(self, patient_id, name, age, emergency_level, symptoms):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.emergency_level = emergency_level
        self.symptoms = symptoms
        self.arrival_time = datetime.now().strftime("%H:%M:%S")
        self.status = "Waiting"
        self.assigned_departments = []

    def __lt__(self, other):
        return self.emergency_level < other.emergency_level

    def __str__(self):
        return f"ID: {self.patient_id} | Name: {self.name} | Age: {self.age} | Emergency Level: {self.emergency_level} | Status: {self.status}"

class BSTNode:
    def __init__(self, patient):
        self.patient = patient
        self.left = None
        self.right = None

class PatientBST:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, patient):
        if self.root is None:
            self.root = BSTNode(patient)
        else:
            self._insert_recursive(self.root, patient)
        self.size += 1

    def _insert_recursive(self, node, patient):
        if patient.patient_id < node.patient.patient_id:
            if node.left is None:
                node.left = BSTNode(patient)
            else:
                self._insert_recursive(node.left, patient)
        else:
            if node.right is None:
                node.right = BSTNode(patient)
            else:
                self._insert_recursive(node.right, patient)

    def search(self, patient_id):
        return self._search_recursive(self.root, patient_id)

    def _search_recursive(self, node, patient_id):
        if node is None:
            return None
        if patient_id == node.patient.patient_id:
            return node.patient
        elif patient_id < node.patient.patient_id:
            return self._search_recursive(node.left, patient_id)
        else:
            return self._search_recursive(node.right, patient_id)

    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.patient)
            self._inorder_recursive(node.right, result)

    def find_min(self):
        if self.root is None:
            return None
        current = self.root
        while current.left:
            current = current.left
        return current.patient

    def find_max(self):
        if self.root is None:
            return None
        current = self.root
        while current.right:
            current = current.right
        return current.patient

    def get_height(self):
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left),
                       self._height_recursive(node.right))

class EmergencyHeap:
    def __init__(self):
        self.heap = []
        self.treated_patients = []

    def _parent(self, index):
        return (index - 1) // 2

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_up(self, index):
        parent = self._parent(index)

        while index > 0 and self.heap[index] < self.heap[parent]:
            self._swap(index, parent)
            index = parent
            parent = self._parent(index)

    def _heapify_down(self, index):
        smallest = index
        left = self._left_child(index)
        right = self._right_child(index)
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def add_patient(self, patient):
        self.heap.append(patient)
        self._heapify_up(len(self.heap) - 1)

    def treat_next_patient(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            patient = self.heap.pop()
        else:
            patient = self.heap[0]
            self.heap[0] = self.heap.pop()
            self._heapify_down(0)

        patient.status = "Being Treated"
        self.treated_patients.append(patient)
        return patient

    def peek_next_patient(self):
        if self.heap:
            return self.heap[0]
        return None

    def get_waiting_count(self):
        return len(self.heap)

    def get_all_waiting(self):
        result = self.heap.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j].emergency_level > result[j + 1].emergency_level:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result

    def is_empty(self):
        return len(self.heap) == 0

class Queue:
    def __init__(self):
        self.items = []
        self.front = 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        item = self.items[self.front]
        self.front += 1

        if self.front > len(self.items) // 2 and self.front > 10:
            self.items = self.items[self.front:]
            self.front = 0
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self.items[self.front]

    def size(self):
        return len(self.items) - self.front

    def is_empty(self):
        return self.front >= len(self.items)

    def get_all(self):
        return self.items[self.front:]

class DepartmentQueue:
    def __init__(self, department_name):
        self.department_name = department_name
        self.queue = Queue()
        self.served_count = 0

    def enqueue(self, patient):
        self.queue.enqueue(patient)
        patient.assigned_departments.append(self.department_name)

    def dequeue(self):
        patient = self.queue.dequeue()
        if patient:
            self.served_count += 1
        return patient

    def peek(self):
        return self.queue.peek()

    def get_queue_length(self):
        return self.queue.size()

    def get_all_patients(self):
        return self.queue.get_all()

    def is_empty(self):
        return self.queue.is_empty()

class HospitalERSystem:
    def __init__(self):
        self.patient_records = PatientBST()
        self.emergency_queue = EmergencyHeap()
        self.lab_queue = DepartmentQueue("Laboratory")
        self.pharmacy_queue = DepartmentQueue("Pharmacy")
        self.radiology_queue = DepartmentQueue("Radiology")
        self.next_patient_id = 1001

    def register_patient(self, name, age, emergency_level, symptoms):
        patient_id = self.next_patient_id
        self.next_patient_id += 1
        patient = Patient(patient_id, name, age, emergency_level, symptoms)
        self.patient_records.insert(patient)
        self.emergency_queue.add_patient(patient)

        print(f"Patient Registered Successfully!")
        print(f"  Patient ID    : {patient_id}")
        print(f"  Name          : {name}")
        print(f"  Age           : {age}")
        print(f"  Emergency Lvl : {emergency_level} ", end="")
        print(self._get_emergency_label(emergency_level))
        print(f"  Symptoms      : {symptoms}")
        print(f"  Arrival Time  : {patient.arrival_time}")
        return patient

    def _get_emergency_label(self, level):
        labels = {
            1: "(CRITICAL - Immediate Attention)",
            2: "(Severe - Urgent)",
            3: "(Moderate - Standard)",
            4: "(Minor - Can Wait)",
            5: "(Non-Urgent - Low Priority)"
        }
        return labels.get(level, "")

    def treat_next_patient(self):
        patient = self.emergency_queue.treat_next_patient()
        if patient:
            print(f"NOW TREATING PATIENT")
            print(f"  {patient}")
            print(f"  Symptoms: {patient.symptoms}")
            return patient
        else:
            print("\nNo patients waiting in emergency queue!")
            return None

    def search_patient(self, patient_id):
        patient = self.patient_records.search(patient_id)
        if patient:
            print(f"PATIENT FOUND")
            print(f"  Patient ID     : {patient.patient_id}")
            print(f"  Name           : {patient.name}")
            print(f"  Age            : {patient.age}")
            print(f"  Emergency Lvl  : {patient.emergency_level}")
            print(f"  Status         : {patient.status}")
            print(f"  Arrival Time   : {patient.arrival_time}")
            print(f"  Symptoms       : {patient.symptoms}")
            print(f"  Departments    : {', '.join(patient.assigned_departments) if patient.assigned_departments else 'None'}")
            return patient
        else:
            print(f"\nPatient with ID {patient_id} not found!")
            return None

    def assign_to_department(self, patient_id, department):
        patient = self.patient_records.search(patient_id)
        if not patient:
            print(f"\nPatient with ID {patient_id} not found!")
            return False

        department_queues = {
            1: self.lab_queue,
            2: self.pharmacy_queue,
            3: self.radiology_queue
        }

        if department in department_queues:
            queue = department_queues[department]
            queue.enqueue(patient)
            print(f"\nPatient {patient.name} assigned to {queue.department_name}")
            return True
        else:
            print("\nInvalid department!")
            return False

    def serve_department_patient(self, department):
        department_queues = {
            1: self.lab_queue,
            2: self.pharmacy_queue,
            3: self.radiology_queue
        }

        if department in department_queues:
            queue = department_queues[department]
            patient = queue.dequeue()
            if patient:
                print(f"\nServing patient {patient.name} at {queue.department_name}")
                return patient
            else:
                print(f"\nNo patients waiting at {queue.department_name}")
                return None
        return None


    def display_emergency_queue(self):
        waiting = self.emergency_queue.get_all_waiting()
        print(f"EMERGENCY QUEUE - PRIORITY ORDER")
        if waiting:
            print(f"{'Priority':<10}{'ID':<10}{'Name':<20}{'Age':<8}{'Status':<15}")
            for i, patient in enumerate(waiting, 1):
                print(f"{i:<10}{patient.patient_id:<10}{patient.name:<20}{patient.age:<8}{patient.status:<15}")
        else:
            print("No patients in emergency queue")


    def display_all_patients(self):
        patients = self.patient_records.inorder_traversal()
        print(f"ALL PATIENT RECORDS (Sorted by Patient ID)")
        if patients:
            print(f"{'ID':<10}{'Name':<20}{'Age':<8}{'Emergency':<12}{'Status':<15}{'Arrival':<12}")
            for patient in patients:
                print(f"{patient.patient_id:<10}{patient.name:<20}{patient.age:<8}{patient.emergency_level:<12}{patient.status:<15}{patient.arrival_time:<12}")
        else:
            print("No patients registered")


    def display_department_queues(self):
        print(f"DEPARTMENT QUEUES STATUS")

        for queue in [self.lab_queue, self.pharmacy_queue, self.radiology_queue]:
            print(f"\n📍 {queue.department_name}")
            print(f"   Waiting: {queue.get_queue_length()} | Served Today: {queue.served_count}")
            if not queue.is_empty():
                print(f"   Patients in queue:")
                for patient in queue.get_all_patients():
                    print(f"      - {patient.name} (ID: {patient.patient_id})")
        print(f"\n{'='*60}")


    def generate_report(self):
        print(f"HOSPITAL ER SYSTEM - COMPREHENSIVE REPORT")
        print(f"\nSTATISTICS:")
        print(f"   • Total Patients Registered : {self.patient_records.size}")
        print(f"   • Patients in Emergency Queue: {self.emergency_queue.get_waiting_count()}")
        print(f"   • Patients Treated Today    : {len(self.emergency_queue.treated_patients)}")
        print(f"   • BST Height               : {self.patient_records.get_height()}")

        print(f"\nDEPARTMENT STATISTICS:")
        for queue in [self.lab_queue, self.pharmacy_queue, self.radiology_queue]:
            print(f"   • {queue.department_name}: {queue.get_queue_length()} waiting, {queue.served_count} served")

        if self.patient_records.size > 0:
            min_patient = self.patient_records.find_min()
            max_patient = self.patient_records.find_max()
            print(f"\nPATIENT ID RANGE:")
            print(f"    Minimum ID: {min_patient.patient_id} ({min_patient.name})")
            print(f"    Maximum ID: {max_patient.patient_id} ({max_patient.name})")

        next_patient = self.emergency_queue.peek_next_patient()
        if next_patient:
            print(f"\n⏭ NEXT PATIENT TO BE TREATED:")
            print(f"   • {next_patient.name} (ID: {next_patient.patient_id}, Emergency Level: {next_patient.emergency_level})")

        print(f"\n{'='*70}")

def display_menu():
    print(f"\n{'x'*60}")
    print(f" HOSPITAL EMERGENCY ROOM MANAGEMENT SYSTEM")
    print(f"{'x'*60}")
    print(f" 1. Register New Patient")
    print(f" 2. Treat Next Emergency Patient ")
    print(f" 3. Search Patient by ID ")
    print(f" 4. Assign Patient to Department ")
    print(f" 5. Serve Patient at Department ")
    print(f" 6. Display Emergency Queue")
    print(f" 7. Display All Patients ")
    print(f" 8. Display Department Queues")
    print(f" 9. Generate System Report")
    print(f" 10. Add Sample Data (Demo)")
    print(f" 0. Exit")
    print(f"{'x'*60}")

def add_sample_data(hospital):
    sample_patients = [
        ("Ahmed Khan", 45, 1, "Chest pain, difficulty breathing"),
        ("Abdul Ali", 28, 3, "High fever, headache"),
        ("Muhammad Uzair", 65, 2, "Severe abdominal pain"),
        ("Fatima Ali", 8, 2, "High fever, seizures"),
        ("Ali Abdullah", 35, 4, "Minor cut on hand"),
        ("Akbar Chaudry", 52, 1, "Heart attack symptoms"),
        ("Ali Gul Pir", 22, 5, "Common cold"),
        ("Zainab Khan", 40, 3, "Diabetic emergency"),
    ]

    print("\nAdding sample patients...")
    for name, age, level, symptoms in sample_patients:
        hospital.register_patient(name, age, level, symptoms)
    print("\n Sample data added successfully!")



def main():
    hospital = HospitalERSystem()

    while True:
        display_menu()
        try:
            choice = int(input("\n  Enter your choice: "))
        except ValueError:
            print("\nPlease enter a valid number!")
            continue

        if choice == 1:
            print("\n--- PATIENT REGISTRATION ---")
            name = input("  Enter patient name: ")
            try:
                age = int(input("  Enter patient age: "))
                print("\n  Emergency Levels:")
                print("    1 - Critical (Immediate)")
                print("    2 - Severe (Urgent)")
                print("    3 - Moderate (Standard)")
                print("    4 - Minor (Can Wait)")
                print("    5 - Non-Urgent (Low Priority)")
                emergency_level = int(input("  Enter emergency level (1-5): "))
                if emergency_level < 1 or emergency_level > 5:
                    print("\nInvalid emergency level! Setting to 3 (Moderate)")
                    emergency_level = 3
            except ValueError:
                print("\nInvalid input! Using default values.")
                age = 30
                emergency_level = 3

            symptoms = input("Enter symptoms: ")
            hospital.register_patient(name, age, emergency_level, symptoms)

        elif choice == 2:
            hospital.treat_next_patient()

        elif choice == 3:
            try:
                patient_id = int(input("\n  Enter Patient ID to search: "))
                hospital.search_patient(patient_id)
            except ValueError:
                print("\nPlease enter a valid Patient ID!")

        elif choice == 4:
            try:
                patient_id = int(input("\n  Enter Patient ID: "))
                print("\n  Departments:")
                print("    1 - Laboratory")
                print("    2 - Pharmacy")
                print("    3 - Radiology")
                dept = int(input("Select department (1-3): "))
                hospital.assign_to_department(patient_id, dept)
            except ValueError:
                print("\n Invalid input!")

        elif choice == 5:
            print("Departments:")
            print("    1 - Laboratory")
            print("    2 - Pharmacy")
            print("    3 - Radiology")
            try:
                dept = int(input("  Select department (1-3): "))
                hospital.serve_department_patient(dept)
            except ValueError:
                print("\nInvalid input!")

        elif choice == 6:
            hospital.display_emergency_queue()

        elif choice == 7:
            hospital.display_all_patients()

        elif choice == 8:
            hospital.display_department_queues()

        elif choice == 9:
            hospital.generate_report()

        elif choice == 10:
            add_sample_data(hospital)

        elif choice == 0:
            print("Thank you for using Hospital ER Management System!")
            print("Goodbye")
            break

        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()