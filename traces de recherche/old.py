from flask import Flask, render_template, jsonify, request, flash
import requests, datetime, time, threading, json

# fonction flask
app = Flask(__name__)
app.secret_key = "test"

# définition des variables 
temps = (datetime.datetime.now()).strftime('%H:%M:%S')

# création de la fonction de répétition
def periodic_execution():
    while True:
        update_json()
        time.sleep(3)
        
# accueil ou l'utilisateur rentre ses 2 url
@app.route('/', methods=["GET", "POST"])
def accueil():
    return render_template("index.html")

@app.route('/add_url', methods=['POST'])
def add_url():
        
    # création des variables du json
    global status, url, temps, site_name

    url = "http://" + request.form["url"]
    
    # Check if the URL already exists in the JSON file
    with open("logs.json", "r") as f:
        contenu = json.load(f)
        for site_name, data in contenu.items():
            if data["url"] == url:
                return "The URL you submitted is already in the list."   
        site_name = "site_" + str(len(json.load(open("logs.json")))+1) # Generate unique site name   
    status = (requests.get(url)).status_code
    temps = (datetime.datetime.now()).strftime('%H:%M:%S')
    contenu =[]
    
    # store the URL in your database 
    with open("logs.json", "r") as f:
        contenu = json.load(f)
    # Access status and time_test for each site

    # Add the new URL to the JSON file
    new_entry = {
                "url": f"{url}",
                "status": [f"{status}"],
                "time_test": [f"{temps}"]
                    }
                
    contenu[site_name] = new_entry
    with open("logs.json", "w") as f:
        json.dump(contenu ,f, indent=4)
        
    # démarrage de la répétition de la fonction update_json()
    thread = threading.Thread(target=periodic_execution)
    thread.daemon = True  # Daemonize the thread so it automatically stops when the main program exits
    thread.start()    

    # return a message indicating the URL has been added
    return "Your URL has been added: " + url

# création de la fonction pour update le fichier json
def update_json():
    global status, url, temps
    temps = (datetime.datetime.now()).strftime('%H:%M:%S')
    with open("logs.json", "r") as f:
        contenu = json.load(f)

    for site_key in contenu:
    # Access status and time_test for each site
        status_value = contenu[site_key]["status"]
        time_test_value = contenu[site_key]["time_test"]
    
        status_value.append(f"{status}")
        time_test_value.append(f"{temps}")


        if len(contenu[site_key]['status']) > 48:
            del contenu[site_key]['status'][0]
        if len(contenu[site_key]['time_test']) > 48:
            del contenu[site_key]['time_test'][0]

    with open("logs.json", "w") as f:
        json.dump(contenu, f, indent=4)
    

       
# initialisation
if __name__=="__main__":
    app.run(host="0.0.0.0", port= 9999, debug=True)
