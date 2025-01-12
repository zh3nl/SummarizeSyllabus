import { use, useState } from "react";
import newUniLogos from "../assets/Uni logos (1).png";
import { useNavigate } from "react-router";

function FileUploader() {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

    const handleFileChange = async (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setMessage("");
        }
    };

  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

    const handleDrop = async (event) => {
        event.preventDefault();
        setIsDragging(false);
        
        const droppedFile = event.dataTransfer.files[0];
        if (droppedFile) {
            setFile(droppedFile);
            setMessage("");
        }
    };

    const uploadFile = async (file) => {

        const formData = new FormData();
        formData.append("file", file);

        try{        
            setLoading(true);
            const response = await fetch("http://localhost:8000/upload", {
                method: "POST",
                body: formData,
            });
            if (response.ok){
                const res = await response.json();
                setMessage(`File uploaded successfully`)
                setFile(null);
                navigate("/courseinfo", {state: {res}})
            }
            else{
                setMessage("Failed to upload file")
            }
        } catch (error){
            console.error("error uploading file: ", error);
            setMessage("error uploading file")
        } finally{
            setLoading(false);
        }
    }

  return (
    <>
      <div className="flex items-center justify-center">
        <div className="flex flex-col items-center space-y-6">
          <h1 className="text-2xl font-semibold text-gray-800">
            Upload Your Syllabus Below
          </h1>
          <div
            className={`w-full max-w-md p-6 border-2 border-dashed rounded-lg cursor-pointer
                        ${
                          isDragging
                            ? "border-blue-500 bg-blue-50"
                            : "border-gray-300"
                        }
                        ${file ? "bg-green-50" : "bg-gray-50"}
                        transition-all duration-200 ease-in-out`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.querySelector('input[type="file"]').click()}
          >
            <input
              type="file"
              onChange={handleFileChange}
              className="hidden"
              accept=".pdf,.doc,.docx,.txt"
            />
            <div className="text-center">
              {file ? (
                <>
                  <p className="text-sm text-gray-600">Selected file:</p>
                  <p className="font-medium">{file.name}</p>
                </>
              ) : (
                <>
                  <p className="text-lg font-medium text-gray-700">
                    Drop your file here or click to browse
                  </p>
                  <p className="mt-2 text-sm text-gray-500">
                    Supported formats: PDF, DOC, DOCX, TXT
                  </p>
                </>
              )}
            </div>
          </div>
          <button 
            onClick={() => uploadFile(file)} 
            className="mt-4 px-6 py-2 bg-blue-500 text-white font-semibold rounded hover:bg-blue-600 transition duration-200">
            Upload File
            </button>
            {loading && (
              <p className="mt-4 text-sm font-medium text-blue-600">
                Uploading file...
              </p>
            )}
            {message && (
                        <p
                            className={`mt-4 text-sm font-medium ${
                                message.includes("successfully")
                                    ? "text-green-600"
                                    : "text-red-600"
                            }`}
                        >
                            {message}
                        </p>
            )}
        </div>
      </div>
      <div className="flex items-center justify-center mt-10">
        <div className=" max-w-4xl w-auto flex flex-col items-center self-center justify-center py-10 px-5 rounded-md border-4 border-slate-500">
          <h2 className="text-2xl text-center">
            Losing points over Syllabus Assignments? Feeling stumped over how to
            lock in?
          </h2>
          <h3 className="text-xl text-center">
            <b>Summarize Syllabus is here to help!</b>
          </h3>
        </div>
      </div>
      <div className="flex flex-col items-center justify-center pt-10">
        <h1 className="text-lg">
          Trust by students from <b>Top</b> Universities and Programs
        </h1>
      </div>
      <div className="flex overflow-hidden px-5">
        <ul className="flex gap-5">
          <li>
            <img
              loading="lazy"
              src={newUniLogos}
              alt=""
              className="h-25 w-auto object-contain object-center self-center shrink-0 max-w-full m-0"
            />
          </li>
        </ul>
      </div>
    </>
  );
 }

export default FileUploader;
