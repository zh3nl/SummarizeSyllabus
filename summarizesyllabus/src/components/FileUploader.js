import { useState } from "react"; 

function FileUploader() {
    const [file, setFile] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const[message, setMessage] = useState("");

    const handleFileChange = async (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            await uploadFile(selectedFile);
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
            await uploadFile(droppedFile);
        }
    };

    const uploadFile = async (file) => {
        const formData = new FormData();
        formData.append("file", file);

        try{        
            const response = await fetch("http://localhost:8000/upload", {
                method: "POST",
                body: formData,
            });
            if (response.ok){
                const res = await response.json();
                setMessage(`File uploaded successfully, path = ${res.filePath}`)
            }
            else{
                setMessage("Failed to upload file")
            }
        } catch (error){
            console.error("error uploading file: ", error);
            setMessage("error uploading file")
        }
    }

    return (
        <div className="flex items-center justify-center">
            <div className="flex flex-col items-center space-y-6">
                <h1 className="text-2xl font-semibold text-gray-800">Upload Your Syllabus Below</h1>
                <div
                    className={`w-full max-w-md p-6 border-2 border-dashed rounded-lg cursor-pointer
                        ${isDragging ? 'border-blue-500 bg-blue-50' : 'bg-gray-100 border-gray-300'}
                        ${file ? 'bg-green-50' : 'bg-gray-50'}
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
                                <p className="text-sm text-gray-700">Selected file:</p>
                                <p className="font-medium">{file.name}</p>
                            </>
                        ) : (
                            <>
                                <p className="text-lg font-medium text-gray-600">
                                    Drop your file here or click to browse
                                </p>
                                <p className="mt-2 text-sm text-gray-500">
                                    Supported formats: PDF, DOC, DOCX, TXT
                                </p>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default FileUploader;