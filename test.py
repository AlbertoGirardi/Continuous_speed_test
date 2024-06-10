class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



print(f"{bcolors.FAIL}ATTENZIONE ERRORE!{bcolors.ENDC}")
print(f"{bcolors.WARNING}ATTENZIONE ERRORE!{bcolors.ENDC}")

print(f"{bcolors.OKBLUE}APPOSTO!{bcolors.ENDC}")
print(f"{bcolors.OKGREEN}APPOSTO!{bcolors.ENDC}")
print(f"{bcolors.BOLD}APPOSTO!{bcolors.ENDC}")
print(f"{bcolors.OKCYAN}APPOSTO!{bcolors.ENDC}")

print('tutto ok')