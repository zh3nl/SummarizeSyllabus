import React from "react";
import { useLocation } from "react-router-dom";

function CourseInfo() {
    const location = useLocation();
    const courseInfo = location.state.summaries; 
    
    return (
        <div>
        <div className="flex justify-center items-center py-10">
        <div className="max-w-4xl" style={{borderRadius: 7, border: "4px solid black",backgroundColor: "#fdf5e6"}}>
        <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
            <h1>Course Information</h1>
            {courseInfo.out2.map((item, index) => (
                <div key={index} style={{ marginBottom: "20px" }}>
                    <h2 style={{ color: "#2c3e50" }}>{item.image_title}</h2>
                    <p style={{ color: "#34495e", lineHeight: "1.6", whiteSpace: "pre-wrap" }}>
                        {item.image_description}
                    </p>
                </div>
            ))}
        </div>

        <h2>---------------</h2>
        <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
            <h1>Course Information</h1>
            {courseInfo.out2.map((item, index) => (
                <div key={index} style={{ marginBottom: "20px" }}>
                    <h2 style={{ color: "#2c3e50" }}>{item.image_title}</h2>
                    <p style={{ color: "#34495e", lineHeight: "1.6", whiteSpace: "pre-wrap" }}>
                        {item.image_description}
                    </p>
                </div>
            ))}
        </div>
        </div>
        </div>
        </div>
    )
}

export default CourseInfo; 