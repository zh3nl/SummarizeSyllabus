import React from "react";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "./CourseInfo.css";

function CourseInfo() {
  const location = useLocation();
  const courseInfo = location.state.summaries;
  const navigate = useNavigate();

  const loginWithGoogle = () => {
    window.location.href = 'http://localhost:8000/login';
  }

  const addEventsToCalendar = async () => {
    try{
      const response = await fetch("http://localhost:8000/add_event", {
          method: "POST",
          header: {
            "Content-Type": "application/json",
          },
      });

      const data = await response.json();
      
      if (response.ok){
        alert("Events successfully added to your Google Calender!");
      } else{
        alert("Failed to add events");
      }
    } catch (error){
      console.error("Error adding events:", error);
      alert("An error occurred while adding events to Google Calender");
    }
  }

  return (
    <div className="container">
      <h1 className="header">Everything You Need To Know About Your Course</h1>

      <div className="section-grid">
        {courseInfo.out2.map((item, index) => (
          <div key={index} className="section">
            <h2 className="subheading">{item.image_title}</h2>
            <p className="paragraph">{item.image_description}</p>
          </div>
        ))}

        {courseInfo.out3.map((item, index) => (
          <div key={index} className="section">
            <h2 className="subheading">{item.image_title}</h2>
            <p className="paragraph">{item.image_description}</p>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
        <button onClick={loginWithGoogle} className="button">
          Login with Google
        </button>
        <button onClick={addEventsToCalendar} className="button">
          Add Events to Google Calendar
        </button>
      </div>

      <button onClick={() => navigate("/upload")} className="button">
        Go Back to Uploading Page
      </button>
    </div>
  );
}

export default CourseInfo;
