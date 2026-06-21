import sys

class ArusTerminalApp:
    def __init__(self):
        # Default application states
        self.buffer_pot = 0.00
        self.gaji_aman_amount = 1000.00 # Target baseline per cycle
        self.current_allowance_left = 0.00 # How much you can actually spend right now
        self.reset_frequency = "Weekly"
        self.income_history = []

    def clear_screen(self):
        print("\n" + "="*45 + "\n")

    def run(self):
        """Main application loop."""
        # Initialize the allowance on first run
        if self.current_allowance_left == 0.00 and self.buffer_pot == 0.00:
            self.current_allowance_left = self.gaji_aman_amount

        while True:
            self.clear_screen()
            print("🚀 ARUS: Cash Flow Smoother for Freelancers")
            print(f"   [Current Budget: RM{self.gaji_aman_amount:.2f} ({self.reset_frequency})]")
            print("-" * 45)
            print(f"   💰 SAFE TO SPEND : RM{self.current_allowance_left:.2f}")
            print(f"   🛡️  BUFFER POT    : RM{self.buffer_pot:.2f}")
            print("-" * 45)
            print("1. 📥 Record Income (Run Smoothing Cycle)")
            print("2. 💸 Record Spend  (Outgoing Transaction)")
            print("3. ⚙️  Settings")
            print("4. ❌ Quit")
            print("-" * 45)
            
            choice = input("Select an option (1-4): ").strip()
            
            if choice == '1':
                self.smoothing_function()
            elif choice == '2':
                self.record_spend_function()
            elif choice == '3':
                self.settings_menu()
            elif choice == '4':
                print("\nTerima kasih using Arus! Staying steady. Goodbye!")
                sys.exit()
            else:
                print("\n⚠️  Invalid choice! Please select 1, 2, 3, or 4.")
                input("\nPress Enter to continue...")

    def smoothing_function(self):
        """Calculates and smooths incoming transaction records."""
        self.clear_screen()
        print("📥 RECORD INCOME (START NEW CYCLE)")
        print(f"Your scheduled target payout is: RM{self.gaji_aman_amount:.2f}")
        print("-" * 45)
        
        try:
            actual_income = float(input("Enter actual income received in MYR (RM): "))
            if actual_income < 0:
                print("⚠️  Income cannot be negative!")
                input("\nPress Enter to return to main menu...")
                return
        except ValueError:
            print("⚠️  Invalid number format!")
            input("\nPress Enter to return...")
            return

        available_to_spend = 0.00

        # Scenario 1: Feast period (Income meets or exceeds target)
        if actual_income >= self.gaji_aman_amount:
            excess = actual_income - self.gaji_aman_amount
            self.buffer_pot += excess
            available_to_spend = self.gaji_aman_amount
            print(f"\n📈 FEAST PERIOD DETECTED!")
            print(f"   - Stashed RM{excess:.2f} safely inside your Buffer Pot.")

        # Scenario 2: Famine period (Income drops below target)
        else:
            shortfall = self.gaji_aman_amount - actual_income
            print(f"\n📉 FAMINE PERIOD DETECTED!")
            print(f"   - Shortfall amount: RM{shortfall:.2f}")
            
            # Check if the buffer can fully cover the difference
            if self.buffer_pot >= shortfall:
                self.buffer_pot -= shortfall
                available_to_spend = self.gaji_aman_amount
                print(f"   - Successfully stabilized! Pulled RM{shortfall:.2f} from the Buffer.")
            # Buffer is insufficient, extract whatever remains
            else:
                available_to_spend = actual_income + self.buffer_pot
                print(f"   - ⚠️ Buffer depleted! Extracted remaining RM{self.buffer_pot:.2f} from Buffer.")
                self.buffer_pot = 0.00

        # Reset the user's spending allowance for the new cycle
        self.current_allowance_left = available_to_spend
        self.income_history.append(actual_income)

        print("-" * 45)
        print(f"💰 New Safe-to-Spend Allowance: RM{self.current_allowance_left:.2f}")
        input("\nPress Enter to return to main menu...")

    def record_spend_function(self):
        """Deducts an outgoing expense from the safe allowance."""
        self.clear_screen()
        print("💸 RECORD SPEND (OUTGOING TRANSACTION)")
        print(f"Available to spend right now: RM{self.current_allowance_left:.2f}")
        print("-" * 45)

        try:
            spend_amount = float(input("Enter amount spent in MYR (RM): "))
            if spend_amount <= 0:
                print("⚠️  Spend amount must be greater than zero!")
                input("\nPress Enter to return to main menu...")
                return
        except ValueError:
            print("⚠️  Invalid number format!")
            input("\nPress Enter to return...")
            return

        # Deduct the amount from the current allowance
        self.current_allowance_left -= spend_amount

        print("\n✅ Transaction recorded.")

        # Check if the user overspent their allowance
        if self.current_allowance_left < 0:
            overspent_amount = abs(self.current_allowance_left)
            print(f"⚠️  You overspent your allowance by RM{overspent_amount:.2f}!")

            # Attempt to cover the overspending using the Buffer Pot
            if self.buffer_pot >= overspent_amount:
                self.buffer_pot -= overspent_amount
                self.current_allowance_left = 0.00
                print(f"🛡️  Covered the deficit by pulling RM{overspent_amount:.2f} from your Buffer Pot.")
            else:
                # Buffer cannot cover the whole deficit
                remaining_deficit = overspent_amount - self.buffer_pot
                print(f"🛡️  Pulled all remaining RM{self.buffer_pot:.2f} from your Buffer Pot.")
                self.buffer_pot = 0.00
                self.current_allowance_left = -remaining_deficit
                print(f"🚨 WARNING: Buffer is empty. You are running a deficit of RM{abs(self.current_allowance_left):.2f}.")
        else:
            print(f"You have RM{self.current_allowance_left:.2f} remaining in your allowance.")

        input("\nPress Enter to return to main menu...")

    def settings_menu(self):
        """Allows users to modify core smoothing frequencies and parameters."""
        while True:
            self.clear_screen()
            print("⚙️  SETTINGS MANAGER")
            print("-" * 45)
            print(f"1. Update Gaji Aman Target Amount (Current: RM{self.gaji_aman_amount:.2f})")
            print(f"2. Change Reset Frequency          (Current: {self.reset_frequency})")
            print("3. Reset Buffer Pot Balance        (Current: RM{self.buffer_pot:.2f})")
            print("4. 🔙 Back to Main Menu")
            print("-" * 45)
            
            choice = input("Select setting to modify (1-4): ").strip()
            
            if choice == '1':
                try:
                    new_amount = float(input("\nEnter new target baseline amount (RM): "))
                    if new_amount <= 0:
                        print("⚠️  Amount must be greater than zero!")
                    else:
                        self.gaji_aman_amount = round(new_amount, 2)
                        print(f"✅ Target baseline updated to RM{self.gaji_aman_amount:.2f}")
                except ValueError:
                    print("⚠️  Invalid format!")
                input("\nPress Enter to continue...")
                
            elif choice == '2':
                print("\nSelect Frequency Option:")
                print("1. Weekly")
                print("2. Monthly")
                freq_choice = input("Select (1-2): ").strip()
                if freq_choice == '1':
                    self.reset_frequency = "Weekly"
                    print("✅ Frequency set to Weekly.")
                elif freq_choice == '2':
                    self.reset_frequency = "Monthly"
                    print("✅ Frequency set to Monthly.")
                else:
                    print("⚠️  No changes made.")
                input("\nPress Enter to continue...")
                
            elif choice == '3':
                confirm = input("\nAre you sure you want to wipe your buffer to RM0.00? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.buffer_pot = 0.00
                    print("✅ Buffer balance cleared.")
                else:
                    print("❌ Operation cancelled.")
                input("\nPress Enter to continue...")
                
            elif choice == '4':
                break
            else:
                print("⚠️  Invalid option.")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = ArusTerminalApp()
    app.run()
