// Open Libs
const tmi = require('tmi.js');
const yaml = require('js-yaml');
const fs   = require('fs');

// Open Config
const config = yaml.load(fs.readFileSync('./config.yml', 'utf8'));

// Formatting words
fmat = []
config["chat_scan"]["words_lookup"].forEach(word => {
	fmat.push(` ${word} `)
})
config["chat_scan"]["words_lookup"] = fmat

// If not enabled exit scan
if (config["chat_scan"] == false){
	console.log("[LOG] Scan disabled - Exit program")
	process.exit()
}

// Create Client for scan
const client = new tmi.Client({
	options: { debug: true, joinInterval : 1000 },
	identity: {
		username: 'TungsteneBot',
		password: "oauth:ggslk6pqrgv94uewfgpgfak14c29bg"
	},
});

// Open previous emotes and messages files
let emotes = require('./data/tchat_emotes.json')
let users = require('./data/tchat_messages.json')
let words = require('./data/messages_lookup.json')
let count = require('./data/messages_count.json')

// Exit if no streamers list
if (config['scan']["streamers"] != false){
	const channels = config['scan']["streamers"]
	client.channels = channels
}
else{
	console.log("[LOG] No streamers list - Exit program")
	process.exit()
}

// Setup delay for beginning and 
console.log(`[LOG] Starting in ${config["requests"]["start"]-Math.floor(Date.now()/1000)} seconds`)
setTimeout(function() {client.connect(); console.log("[LOG] Logged")}, (config["requests"]["start"]-Math.floor(Date.now()/1000))*1000)
console.log(`[LOG] Ending in ${config["requests"]["end"]-Math.floor(Date.now()/1000)} seconds`)
setTimeout(function() {client.disconnect(); console.log("[LOG] Unlogged"); process.exit()}, (config["requests"]["end"]-Math.floor(Date.now()/1000))*1000)

// Define logs (warn for minimized, info for all)
client.log.setLevel('warn');

// Event : On every messages
client.on('message', (channel, tags, message, self) => {

	// Words scan
	if(CheckMessage(` ${message.toLowerCase()} `,config["chat_scan"]["words_lookup"])){
		if(!words[tags["username"]]){
			words[tags["username"]] = []
		}
		words[tags["username"]].push(message)
	}
	
	if(config['chat_scan']['words_count'] != []){
		config["chat_scan"]["words_count"].forEach(emote => {
			if(!count[channel]){
				count[channel] = {}
			}
			if(!count[channel][emote]){
				count[channel][emote] = 0
			}
			count[channel][emote] += CheckEmote(` ${message.toLowerCase()} `,emote)
		})
	}

	// Create channel dict if didn't exist
	if(!users[channel]){
		users[channel] = {}
	}

	// Create user dict in channel if didn't exist and add 1
	if(users[channel][tags['username']]){
    	users[channel][tags['username']] += 1
	}
	else{
		users[channel][tags['username']] = 1
	}

	// Message contain emote
	if(tags['emotes']){
		// Create channel dict if didn't exist
		if(!emotes[channel]){
			emotes[channel] = {}
		}

		// Create user dict in channel if didn't exist and add 1
		if(!emotes[channel][tags['username']]){
			emotes[channel][tags['username']] = {}
		}
		Object.keys(tags["emotes"]).forEach(emote => { // If Emote : for each
			if(emotes[channel][tags['username']][emote]){ // Adding length if already added
	    		emotes[channel][tags['username']][emote] += tags['emotes'][emote].length
			}
			else{ // Creating it with length
				emotes[channel][tags['username']][emote] = tags['emotes'][emote].length
			}
		})
	}
});

// Function to update files
function write_file() { 
	messages_list = JSON.stringify(users, null, 4);
	fs.writeFile("./data/tchat_messages.json",messages_list,()=>{})

	emotes_list = JSON.stringify(emotes, null, 4);
	fs.writeFile("./data/tchat_emotes.json",emotes_list,()=>{})

	words_list = JSON.stringify(words, null, 4);
	fs.writeFile("./data/messages_lookup.json",words_list,()=>{})

	count_list = JSON.stringify(count, null, 4);
	fs.writeFile("./data/messages_count.json",count_list,()=>{})
}

// Function to check messages
function CheckMessage(message,words){
  return words.some(word => message.includes(word));
}
function CheckEmote(message,emote){
	let list = message.match(emote || [])
	if(list != null){
		return list.length
	}
	else{
		return 0
	}
}

// Call for every update
setInterval(function () {write_file(); return true}, 30000);
