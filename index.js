import express from "express";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";
import multer from "multer";

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "public/uploads/");   // 👈 save here
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + "-" + file.originalname);
  },
});

const upload = multer({ storage: storage });

// Fix for __dirname in ES Modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const videoPath = path.join(__dirname, "public");

// serve static files (HTML + video)
app.use(express.static(path.join(__dirname, "public")));

app.get("/",(req,res)=>{
    res.render("index.ejs")
});

app.post("/upload", upload.single("video"), (req, res) => {
  const uploadedFilePath = req.file.path; 
  console.log("Uploaded file:", uploadedFilePath);
  const pythonScriptPath = path.join(__dirname, "pushup.py");
  const pythonProcess = spawn("python", [pythonScriptPath, uploadedFilePath]);
  

  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`Python error: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`Python process exited with code ${code}`);
    res.redirect("/show-video");
  });
});

app.get("/run-python", (req, res) => {
  const python = spawn("python", ["pushup.py"]);

  python.stdout.on("data", (chunk) => {
    console.log(`Python output: ${chunk}`);
  });

  python.stderr.on("data", (chunk) => {
    console.log(`Python log: ${chunk}`);
  });

  python.on("close", (code) => {
    console.log(`Python finished with code ${code}`);
    setTimeout(() => {
    res.redirect("/show-video");
  }, 1000);
  });
});

app.get("/show-video", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "video.html"));
});

app.listen(3000, () => console.log("✅ Server running at http://localhost:3000"));
