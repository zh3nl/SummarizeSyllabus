import React, { createContext, useContext, useState, useEffect } from "react";

const SummariesContext = createContext();

export const SummariesProvider = ({ children }) => {
    const [summaries, setSummaries] = useState(null);

    useEffect(() => {
        const storedSummaries = localStorage.getItem("summaries");
        if (storedSummaries) {
          setSummaries(JSON.parse(storedSummaries));
        }
      }, []);

      const updateSummaries = (data) => {
        setSummaries(data);
        localStorage.setItem("summaries", JSON.stringify(data));
      };
  
    return (
      <SummariesContext.Provider value={{ summaries, updateSummaries }}>
        {children}
      </SummariesContext.Provider>
    );
  };
  
export const useSummaries = () => useContext(SummariesContext);