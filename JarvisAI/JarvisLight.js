const {exec} = require("child_process");
const page = require("express")();
const path = require("path");
const port = 2004;

page.get("/", (req, res) => {
    res.send(200)
});

page.post("/", (req, res) => {
    res.send(200);
});

page.post("/:Command", (req, res) => {
    console.log(`Command : ${req.params.Command}`), req.params.Command;
    if(req.params.Command == "LightOn"){
        exec("python C:/Users/a0988/OneDrive/Desktop/Jarvis/features/Lighton.py");
        console.log("ON");
    }else if(req.params.Command == "LightOff"){
        exec("python C:/Users/a0988/OneDrive/Desktop/Jarvis/features/Lightoff.py");
        console.log("OFF");
    };
    res.send(200);
});

page.listen(port, console.log("Sever listening in "+port));