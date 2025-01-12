import React from "react";
import { useNavigate } from "react-router-dom";
import { useSummaries } from "./SummariesContext";
import "./CourseInfo.css";

function CourseInfo() {
  const { summaries } = useSummaries();
  const navigate = useNavigate();

  console.log("Summaries in CourseInfo:", summaries);

  const addEventsToCalendar = async () => {
    window.location.href = 'http://localhost:8000/login';
  }

  if (!summaries) {
    return (
      <div className="container">
        <h1 className="header">No Course Data Available</h1>
        <p className="paragraph">Please upload a syllabus to see course details.</p>
        <button onClick={() => navigate("/upload")} className="button">
          Go Back to Uploading Page
        </button>
      </div>
    );
  }

  return (
    <div className="container">
      <h1 className="header">Everything You Need To Know About Your Course</h1>

      <div className="section-grid">
        {summaries.out2.map((item, index) => (
          <div key={index} className="section">
            <h2 className="subheading">{item.image_title}</h2>
            <p className="paragraph">{item.image_description}</p>
          </div>
        ))}

        {summaries.out3.map((item, index) => (
          <div key={index} className="section">
            <h2 className="subheading">{item.image_title}</h2>
            <p className="paragraph">{item.image_description}</p>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
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
