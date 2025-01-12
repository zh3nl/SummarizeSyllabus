import React from "react";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "./CourseInfo.css";

function CourseInfo() {
  const location = useLocation();
  const courseInfo = location.state.summaries;
  const navigate = useNavigate();

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

      {/* Navigation Button */}
      <button onClick={() => navigate("/upload")} className="button">
        Go Back to Uploading Page
      </button>
    </div>
  );
}

export default CourseInfo;
