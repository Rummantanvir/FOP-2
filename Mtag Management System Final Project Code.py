import pandas as pd
import random

# Dataframe to store the vehicle information
vehicles = pd.DataFrame(columns=["Mtag Number", "CNIC", "Number Plate", "Owner", "Contact", "Balance", "City"])

# Dataframe to store toll information
toll_info = pd.DataFrame(columns=["City", "Toll Fee"])

# Function to save vehicles data to a CSV file
def save_to_excel():
    vehicles.to_csv(r"C:\Programming - Pycharm\MTAGG.csv", index=False)  # Use raw string for the file path
    toll_info.to_csv(r"C:\Programming - Pycharm\TollInfo.csv", index=False)
    print("Vehicles data and toll info have been saved.")

# Function to load vehicles data from CSV file
def load_from_excel():
    try:
        vehicles_data = pd.read_csv(r"C:\Programming - Pycharm\MTAGG.csv")  # Use raw string for the file path
        toll_data = pd.read_csv(r"C:\Programming - Pycharm\TollInfo.csv")
        return vehicles_data, toll_data
    except FileNotFoundError:
        print("No previous data found.")
        return pd.DataFrame(
            columns=["Mtag Number", "CNIC", "Number Plate", "Owner", "Contact", "Balance", "City"]), pd.DataFrame(
            columns=["City", "Toll Fee"])

# Registering a new vehicle
def register_vehicle(cnic, number_plate=None, car_model=None, owner_name=None, contact=None, city=None):
    if cnic in vehicles["CNIC"].values:
        print("This CNIC is already registered.")
        choice = input("Do you want to register another vehicle under the same CNIC? (yes/no): ").lower()
        if choice == "yes":
            owner_name = vehicles.loc[vehicles["CNIC"] == cnic, "Owner"].values[0]
            contact = vehicles.loc[vehicles["CNIC"] == cnic, "Contact"].values[0]
            city = vehicles.loc[vehicles["CNIC"] == cnic, "City"].values[0]
        else:
            print("No additional vehicle registered.")
            return
    else:
        owner_name = owner_name or input("Enter Owner Name: ")
        contact = contact or input("Enter Contact Number (XXXX-XXXXXXX): ")
        city = city or input("Enter City: ")

    number_plate = number_plate or input("Enter Number Plate: ")
    car_model = car_model or input("Enter Car Model: ")

    mtag_number = random.randint(1000, 9999)
    new_vehicle = {
        "Mtag Number": mtag_number,
        "CNIC": cnic,
        "Number Plate": number_plate,
        "Car Model": car_model,
        "Owner": owner_name,
        "Contact": contact,
        "Balance": 0,
        "City": city,
    }
    vehicles.loc[len(vehicles)] = new_vehicle
    print(f"Vehicle with CNIC {cnic} has been registered successfully.")
    print(f"Vehicle Mtag Number: {mtag_number}")


# Function to add toll information based on city
def add_toll_info(city, toll_fee):
    if city not in toll_info["City"].values:
        new_toll = {"City": city, "Toll Fee": toll_fee}
        toll_info.loc[len(toll_info)] = new_toll
        print(f"Toll fee for {city} has been added with fee ${toll_fee}.")
    else:
        print(f"Toll fee for {city} already exists.")

# Displaying all vehicles that are registered
def display_vehicles():
    if vehicles.empty:
        print("No vehicles registered.")
    else:
        print(vehicles)


# Add balance to a vehicle's account
def add_balance(cnic, mtag_number, amount):
    if cnic in vehicles["CNIC"].values and mtag_number in vehicles["Mtag Number"].values:
        if not vehicles[(vehicles["CNIC"] == cnic) & (vehicles["Mtag Number"] == mtag_number)].empty:
            vehicles.loc[(vehicles["CNIC"] == cnic) & (vehicles["Mtag Number"] == mtag_number), "Balance"] += amount
            new_balance = vehicles.loc[(vehicles["CNIC"] == cnic) & (vehicles["Mtag Number"] == mtag_number), "Balance"].values[0]
            print(f"Added ${amount} to vehicle with Mtag Number {mtag_number}. \nNew balance: ${new_balance}.")
        else:
            print("The provided CNIC and Mtag Number do not match.")
    else:
        print("Invalid CNIC or Mtag Number.")


# Find and display vehicle details based on Mtag number
def display_by_mtag(mtag_number):
    vehicle = vehicles[vehicles["Mtag Number"] == mtag_number]
    if not vehicle.empty:
        print("Vehicle details:")
        print(vehicle)
    else:
        print("No vehicle found with the given Mtag number.")


# Calculate and deduct toll based on the city
def calculate_and_deduct_toll(cnic, mtag_number, city):
    if cnic in vehicles["CNIC"].values and mtag_number in vehicles["Mtag Number"].values:
        if not vehicles[(vehicles["CNIC"] == cnic) & (vehicles["Mtag Number"] == mtag_number)].empty:
            toll_fee = toll_info.loc[toll_info["City"] == city, "Toll Fee"].values
            if toll_fee.size > 0:
                toll_fee = toll_fee[0]
                current_balance = vehicles.loc[(vehicles["CNIC"] == cnic) & (vehicles["Mtag Number"] == mtag_number), "Balance"].values[0]
                if current_balance >= toll_fee:
                    vehicles.loc[(vehicles["CNIC"] == cnic) & (vehicles["Mtag Number"] == mtag_number), "Balance"] -= toll_fee
                    print(f"Toll fee of ${toll_fee} for city {city} has been deducted from vehicle with Mtag Number {mtag_number}.")
                else:
                    print("Insufficient balance for toll deduction.")
            else:
                print(f"No toll fee information found for city {city}.")
        else:
            print("The provided CNIC and Mtag Number do not match.")
    else:
        print("Invalid CNIC or Mtag Number.")


# Main code that runs with a while loop until user exits
while True:
    print("\nOptions for Mtag management:")
    print("1. Register a vehicle")
    print("2. Display all vehicles")
    print("3. Add balance")
    print("4. Display vehicle details by Mtag number")
    print("5. Add Toll Information of City")
    print("6. Calculate and Deduct Toll")
    print("7. Save and Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        cnic = input("Enter CNIC (XXXXX-XXXXXXX-X): ")
        register_vehicle(cnic)
    elif choice == "2":
        display_vehicles()
    elif choice == "3":
        cnic = input("Enter CNIC (XXXXX-XXXXXXX-X): ")
        if cnic in vehicles["CNIC"].values:
            mtag_number = int(input("Enter Mtag Number: "))
            if mtag_number in vehicles.loc[vehicles["CNIC"] == cnic, "Mtag Number"].values:
                amount = float(input("Enter amount to add ($): "))
                add_balance(cnic, mtag_number, amount)
            else:
                print("Invalid Mtag Number. Please try again.")
        else:
            print("Invalid CNIC. The vehicle is not registered.")
    elif choice == "4":
        mtag_number = int(input("Enter Mtag Number: "))
        display_by_mtag(mtag_number)
    elif choice == "5":
        city = input("Enter the city for the toll information: ")
        toll_fee = float(input("Enter the toll fee for this city: "))
        add_toll_info(city, toll_fee)
    elif choice == "6":
        cnic = input("Enter CNIC (XXXXX-XXXXXXX-X): ")
        if cnic in vehicles["CNIC"].values:
            mtag_number = int(input("Enter Mtag Number: "))
            if mtag_number in vehicles.loc[vehicles["CNIC"] == cnic, "Mtag Number"].values:
                city = input("Enter the city name for toll deduction: ")
                calculate_and_deduct_toll(cnic, mtag_number, city)
            else:
                print("Invalid Mtag Number. Please try again.")
        else:
            print("Invalid CNIC. The vehicle is not registered.")
    elif choice == "7":
        save_to_excel()
        print("Exiting system...")
        break
    else:
        print("Invalid choice. Please try again.")
