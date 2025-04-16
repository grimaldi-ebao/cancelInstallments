import logging
import json
from datetime import datetime, time

limit=1000
invalidate_prefix= "'-4'"
not_in = ' "2369414227", "2369414228", "2369424175", "2369424229", "2369444139", "2369454574", "2369454585", "2369454587", "2369464296", "2369464297", "2369464300", "2369464302", "2369474219", "2369474220", "2369474223", "2369484194", "2369484210", "2369484211", "2369494324", "2369494379", "2369504138", "2369504139", "2369504141", "2369504143", "2369514178", "2369514179", "2369514183", "2369514184", "2369524421", "2369524422", "2369534335", "2369544337", "2369544340", "2369554152", "2369564269", "2369574255", "2369574256", "2369604204", "2369604205", "2369614381", "2369624398", "2369654309", "2369654346", "2369654347", "2369674129", "2369694215", "2369694216", "2369714257", "2369724057", "2369724077", "2369724081", "2369724082", "2369733995", "2369734009", "2369734011", "2369734012", "2387712382", "2387721976", "2387721978", "2387721979", "2387721980", "2387732188", "2387742342", "2387742346", "2387752902", "2387752903", "2387752905", "2387752906", "2387762279", "2387762280", "2387762281", "2387802153", "2387802155", "2387802156", "2387812729", "2387812730", "2387812731", "2387821898", "2387821901", "2387821902", "2387832062", "2387842038", "2387852705", "2387861864", "2387861870", "2387861873", "2387861874", "2387861875", "2387861876", "2387891891", "2387911905", "2387942074", "2387942079", "2387942080", "2387942081", "2387952426", "2387983059", "2387983060", "2387992030", "2388052542", "2388052543", "2388061927", "2388061928", "2388081675", "2388081678", "2388081679", "2388081682", "2388092151", "2388122474", "2388122475" '

def process_strings(string_list):
    temp = ""  # Variable to hold the concatenated strings
    count = 0  # Counter for tracking the number of strings processed

    for string in string_list:
        # Append the string to the 'temp' variable, separated by commas
        if temp:
            temp += f", '{string}'"
        else:
            temp = f"'{string}'"

        count += 1

        # Generate a file when the specified limit is reached
        if count % limit == 0:
            file_name = f"out/output_{count // limit}.txt"
            with open(file_name, "w") as file:
                file.write(f"####################\n")
                file.write(f"use hdibrazil_pa;\n")
                file.write(f"\n")
                file.write(f"UPDATE t_pa_pl_policy SET policy_no=CONCAT('-4', policy_no), `PROPOSAL_STATUS` ='-1', `POLICY_STATUS` ='-1' WHERE `POLICY_NO` in ({temp});\n\n")
                file.write(f"UPDATE t_pa_pl_policy_l SET policy_no=CONCAT('-4', policy_no),`PROPOSAL_STATUS` ='-1',`POLICY_STATUS` ='-1' WHERE `POLICY_NO` in  ({temp});\n\n")
                file.write(f"UPDATE t_pa_endo_endorsement SET endo_no=CONCAT('-4', endo_no), policy_no=CONCAT('-4', policy_no),`ENDO_STATUS` ='-1' WHERE `POLICY_NO` in  ({temp});\n\n")
                file.write(f"\n")
                file.write(f"use hdibrazil_tenant;\n")
                file.write(f"\n")
                file.write(f"UPDATE t_pa_settle_settlement  SET POLICY_NO=CONCAT('-4', policy_no),ENDO_NO=CONCAT('-4', ENDO_NO) WHERE policy_no in ({temp});\n\n")
                file.write(f"UPDATE t_pa_settle_settlement_item SET certificate_policy_no = CONCAT('-4', certificate_policy_no) WHERE certificate_policy_no in  ({temp});\n\n")
                file.write(f"UPDATE t_pa_settle_settlement_item SET certificate_endo_no = REPLACE(certificate_endo_no,'-4-4','-4') WHERE certificate_policy_no LIKE '%-4%';\n\n")
                file.write(f"UPDATE t_pa_settle_settlement_item SET certificate_endo_no = CONCAT('-4', certificate_endo_no) WHERE certificate_policy_no LIKE '-4%' and certificate_endo_no IS NOT NULL AND ITEM_ID NOT IN ({not_in});\n\n")
                file.write(f"\n")

            print(f"File '{file_name}' generated.")
            temp = ""  # Reset 'temp' after writing to the file

        # Process the remaining strings if the count is not a multiple of the limit
        if temp:
            file_name = f"out/output_{(count // limit) + 1}.txt"
            with open(file_name, "w") as file:
                file.write(f"use hdibrazil_pa;\n")
                file.write(f"UPDATE t_pa_pl_policy SET policy_no=CONCAT('-4', policy_no), `PROPOSAL_STATUS` ='-1', `POLICY_STATUS` ='-1' WHERE `POLICY_NO` in ({temp});\n")
                file.write(f"UPDATE t_pa_pl_policy_l SET policy_no=CONCAT('-4', policy_no),`PROPOSAL_STATUS` ='-1',`POLICY_STATUS` ='-1' WHERE `POLICY_NO` in  ({temp});\n")
                file.write(f"UPDATE t_pa_endo_endorsement SET endo_no=CONCAT('-4', endo_no), policy_no=CONCAT('-4', policy_no),`ENDO_STATUS` ='-1' WHERE `POLICY_NO` in  ({temp});\n")
                file.write(f"use hdibrazil_tenant;\n")
                file.write(f"UPDATE t_pa_settle_settlement  SET POLICY_NO=CONCAT('-4', policy_no),ENDO_NO=CONCAT('-4', ENDO_NO) WHERE policy_no in ({temp});\n")
                file.write(f"UPDATE t_pa_settle_settlement_item SET certificate_policy_no = CONCAT('-4', certificate_policy_no) WHERE certificate_policy_no in  ({temp});\n")
                file.write(f"UPDATE t_pa_settle_settlement_item SET certificate_endo_no = REPLACE(certificate_endo_no,'-4-4','-4') WHERE certificate_policy_no LIKE '%-4%';\n")
                file.write(f"UPDATE t_pa_settle_settlement_item SET certificate_endo_no = CONCAT('-4', certificate_endo_no) WHERE certificate_policy_no LIKE '-4%' and certificate_endo_no IS NOT NULL AND ITEM_ID NOT IN ({not_in});\n\n")

        print(f"File '{file_name}' generated.")


def read_json_file(file_path):
    try:
        # Open the JSON file and load its content
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not in valid JSON format.")
        return None


def logger():
    #format = "%(asctime)s: %(message)s"
    now = datetime.now()

    logging.basicConfig(
        filename='logfile{0}.log'.format(now.strftime("%Y%m%d_%H%M%S")),  # Name of the log file
        level=logging.DEBUG,  # Set the minimum logging level
        format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
        #datefmt="%H:%M:%S"
    )

def start():
    logger()
    content = read_json_file('data/invalidate3.json')
    print(len(content['Documents']))
    process_strings(content['Documents'])
    # println(content)
    #process(content)
    # run_in_threads(content)

if __name__ == '__main__':
    try:
        start()
    except:
        print("main error...")
    finally:
        print('Finish')