## 🛠️ Build & Run Instructions

Follow the steps below to build and execute the project:

### 1️⃣ Modify Source Code

Update the `main.c` file as per your requirements.

---

### 2️⃣ Clean Previous Build

Delete the existing `build` folder (if present) to ensure a clean build.

---

### 3️⃣ Build the Project

Open a terminal (Command Prompt) in the project directory and run:

```
cmake -B build -G "Unix Makefiles"
cmake --build build
```

---

### 4️⃣ Run the Application

* Navigate to the `build` folder
* Execute the generated file:

```
app.exe
```

---

## 📦 Requirements

### CMake Installation

Download and install CMake from the official website:

👉 https://cmake.org/download/

* Recommended: **Windows x64 Installer**
* Example version: `cmake-4.0.1-windows-x86_64.msi`

---

## 🔗 Dependencies

* cJSON Library: https://github.com/davegamble/cjson

---

## 📌 Notes

* Ensure CMake is added to your system PATH during installation
* Always perform a clean build if you encounter errors
* Compatible with Windows environments using Unix Makefiles

---
