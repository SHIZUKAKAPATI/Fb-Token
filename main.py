// facebook-token-checker.js
import express from "express";
import fetch from "node-fetch";
const app = express();
app.use(express.json());
const PORT = process.env.PORT || 3000;
// Serve frontend HTML
app.get("/", (req, res) => {
  res.send(<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🔥 𝐑𝐊 𝐑𝐀𝐉𝐀 𝐗𝐕𝐃 𝐇𝟑𝐑𝟑 𝐓𝐎𝐊𝟑𝐍 𝐃𝟑𝐊𝐇 𝟗𝟗𝐏𝐍𝐀 𝐓𝐎𝐊𝟑𝐍 𝐂𝐇𝟑𝐂𝐊 𝐊𝟗𝐑  🔥</title>
<style>
body{font-family:Segoe UI,Tahoma,Geneva,Verdana,sans-serif;background:linear-gradient(135deg,#ffcc00,#ff9900);display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
.checker-container{background:rgba(255,255,255,0.15);backdrop-filter:blur(12px);padding:30px;border-radius:20px;box-shadow:0 0 25px rgba(0,0,0,0.4);width:500px;text-align:center;color:#fff}
input{width:85%;padding:12px;margin:10px 0;border-radius:12px;border:none;outline:none}
button{padding:10px 18px;background:#ff6600;border:none;border-radius:10px;color:white;font-weight:bold;cursor:pointer;transition:.3s;margin:5px 3px}
button:hover{background:#cc5200}
#result{margin-top:20px;text-align:left;background:rgba(255,255,255,0.2);padding:15px;border-radius:12px;word-break:break-all}
img.profile-pic{width:80px;height:80px;border-radius:50%;border:2px solid #fff;margin-bottom:10px}
a{color:#fff;text-decoration:underline}
.time{font-size:12px;margin-top:5px;color:#ddd}
.log{background:rgba(0,0,0,0.2);padding:8px;margin:5px 0;border-radius:8px;font-family:monospace;max-height:150px;overflow-y:auto}
</style>
</head>
<body>
<div class="checker-container">
<h2>Facebook Token Checker</h2>
<input type="text" id="tokenInput" placeholder="Enter your token">
<br>
<button onclick="startChecking()">Start Auto-Check</button>
<button onclick="stopChecking()">Stop Auto-Check</button>
<div id="result"></div>
<div class="log" id="log"></div>
</div>
<audio id="alertSound" src="https://www.soundjay.com/button/beep-07.mp3" preload="auto"></audio>
<script>
let intervalId=null;
function logMessage(msg){const logDiv=document.getElementById('log');const time=new Date().toLocaleTimeString();logDiv.innerHTML+=\[\${time}] \${msg}<br>\;logDiv.scrollTop=logDiv.scrollHeight;}
async function checkToken(){
const token=document.getElementById('tokenInput').value.trim();
const resultDiv=document.getElementById('result');
if(!token){alert("Please enter a token!");return;}
logMessage("Checking token...");
try{
const res=await fetch("/check-token",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({token})});
const data=await res.json();
if(res.status!==200){logMessage(data.error);document.getElementById('alertSound').play();stopChecking();alert("Token invalid/expired");return;}
const now=new Date();
const timeStr=now.toLocaleString();
let groupsHTML="",gcIds="";
if(data.groups.length>0){groupsHTML="<ul>";data.groups.forEach(g=>{groupsHTML+=\<li>\${g.name} (GC UID: \${g.id})</li>\;gcIds+=\\${g.id}, \});groupsHTML+="</ul>";gcIds=gcIds.slice(0,-2);}else{groupsHTML="No groups found or permission denied.";}
resultDiv.innerHTML=\
<center><img class="profile-pic" src="\${data.profilePic}" alt="Profile Picture"></center>
<b>Name:</b> \${data.name} <button onclick="copyToClipboard('\${data.name}')">Copy</button><br>
<b>UID:</b> \${data.uid} <button onclick="copyToClipboard('\${data.uid}')">Copy</button><br>
<b>Profile URL:</b> <a href="\${data.profileURL}" target="_blank">\${data.profileURL}</a> <button onclick="copyToClipboard('\${data.profileURL}')">Copy</button><br>
<b>Groups:</b> \${groupsHTML} <button onclick="copyToClipboard('\${gcIds}')">Copy GC IDs</button>
<div class="time">Checked at: \${timeStr}</div>\`;
logMessage("Result displayed successfully.");
}catch(err){resultDiv.innerHTML="Error fetching data.";logMessage("Error fetching data. Possibly server down or token issue.");console.error(err);document.getElementById('alertSound').play();stopChecking();}

}
function copyToClipboard(text){navigator.clipboard.writeText(text).then(()=>alert("Copied!")).catch(()=>alert("Failed to copy."));}
function startChecking(){if(intervalId) clearInterval(intervalId);checkToken();intervalId=setInterval(checkToken,30000);logMessage("Auto-check started (every 30s).");}
function stopChecking(){if(intervalId){clearInterval(intervalId);intervalId=null;logMessage("Auto-check stopped.");}}
</script>
</body>
</html>);
});
// Token check route
app.post("/check-token", async (req, res) => {
  const { token } = req.body;
  if(!token) return res.status(400).json({error:"Token missing"});
  try{
    const userRes = await fetch(https://graph.facebook.com/me?fields=id,name,picture.width(200).height(200)&access_token=${token});
    const userData = await userRes.json();
    if(userData.error) return res.status(400).json({error:userData.error.message});
    const groupsRes = await fetch(https://graph.facebook.com/me/groups?access_token=${token});
    const groupsData = await groupsRes.json();
    let gcIds = [];
    if(groupsData.data && groupsData.data.length>0){
      gcIds = groupsData.data.map(g=>({name:g.name,id:g.id}));
    }
    res.json({
      name:userData.name,
      uid:userData.id,
      profilePic:userData.picture.data.url,
      profileURL:https://facebook.com/${userData.id},
      groups:gcIds
    });
  }catch(err){
    res.status(500).json({error:"Server error"});
  }
});
app.listen(PORT, ()=>console.log(Server running on port ${PORT}`));<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🔥 𝐑𝐊 𝐑𝐀𝐉𝐀 𝐗𝐕𝐃 𝐇𝟑𝐑𝟑 𝐓𝐎𝐊𝟑𝐍 𝐃𝟑𝐊𝐇 𝟗𝟗𝐏𝐍𝐀 𝐓𝐎𝐊𝟑𝐍 𝐂𝐇𝟑𝐂𝐊 𝐊𝟗𝐑  🔥</title>
<style>
body{font-family:Segoe UI,Tahoma,Geneva,Verdana,sans-serif;background:linear-gradient(135deg,#ffcc00,#ff9900);display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
.checker-container{background:rgba(255,255,255,0.15);backdrop-filter:blur(12px);padding:30px;border-radius:20px;box-shadow:0 0 25px rgba(0,0,0,0.4);width:500px;text-align:center;color:#fff}
input{width:85%;padding:12px;margin:10px 0;border-radius:12px;border:none;outline:none}
button{padding:10px 18px;background:#ff6600;border:none;border-radius:10px;color:white;font-weight:bold;cursor:pointer;transition:.3s;margin:5px 3px}
button:hover{background:#cc5200}
#result{margin-top:20px;text-align:left;background:rgba(255,255,255,0.2);padding:15px;border-radius:12px;word-break:break-all}
img.profile-pic{width:80px;height:80px;border-radius:50%;border:2px solid #fff;margin-bottom:10px}
a{color:#fff;text-decoration:underline}
.time{font-size:12px;margin-top:5px;color:#ddd}
.log{background:rgba(0,0,0,0.2);padding:8px;margin:5px 0;border-radius:8px;font-family:monospace;max-height:150px;overflow-y:auto}
</style>
</head>
<body>
<div class="checker-container">
<h2>Facebook Token Checker</h2>
<input type="text" id="tokenInput" placeholder="Enter your token">
<br>
<button onclick="startChecking()">Start Auto-Check</button>
<button onclick="stopChecking()">Stop Auto-Check</button>
<div id="result"></div>
<div class="log" id="log"></div>
</div>
<audio id="alertSound" src="https://www.soundjay.com/button/beep-07.mp3" preload="auto"></audio>
<script>
let intervalId=null;
function logMessage(msg){const logDiv=document.getElementById('log');const time=new Date().toLocaleTimeString();logDiv.innerHTML+=\
