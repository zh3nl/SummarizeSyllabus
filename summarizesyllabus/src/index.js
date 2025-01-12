import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import CourseInfo from "./components/CourseInfo";
import FileUploader from "./components/FileUploader";
import { SummariesProvider} from "./components/SummariesContext";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  }, {
    path: "/courseinfo",
    element: <CourseInfo />,
  }, {
    path: "/upload",
    element: <FileUploader />,
  }
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <SummariesProvider>
      <RouterProvider router={router} />
    </SummariesProvider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
