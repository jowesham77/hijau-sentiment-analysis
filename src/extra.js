// export NODE_OPTIONS=--openssl-legacy-provider

import React, { useState } from "react";
import "./App.css";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const mockData = [
  { date: "2024-02-13", index: 45 },
  { date: "2024-02-14", index: 50 },
  { date: "2024-02-15", index: 55 },
  { date: "2024-02-16", index: 60 },
  { date: "2024-02-17", index: 53 },
  { date: "2024-02-18", index: 58 },
  { date: "2024-02-19", index: 62 }
];

const newsData = [
  {
    category: "Climate",
    date: "2/23/25",
    articles: [
      { text: "• Utah’s Bitcoin reserve bill advances to Senate standing committee.", source: "#" },
      { text: "• Bitcoin market is 'behaving cautiously' not seen since before US elections, says K33.", source: "#" },
      { text: "• Strategy announces $2 billion conversion rate offering to fuel future bitcoin purchases.", source: "#" },
      { text: "• Bitcoin network activity hits 12-month lows as transactions drop 50% from peak.", source: "#" },
      { text: "• Bitcoin struggles with heightened volatility as US tariffs and Fed policy fuel market uncertainty.", source: "#" },
      { text: "• Hong Kong confirms Bitcoin and Ether can be used to secure wealth for investment visa.", source: "#" }
    ]
  },
  {
    category: "Energy",
    date: "2/23/25",
    articles: [
      { text: "• Utah’s Bitcoin reserve bill advances to Senate standing committee.", source: "#" },
      { text: "• Bitcoin market is 'behaving cautiously' not seen since before US elections, says K33.", source: "#" },
      { text: "• Strategy announces $2 billion conversion rate offering to fuel future bitcoin purchases.", source: "#" },
      { text: "• Bitcoin network activity hits 12-month lows as transactions drop 50% from peak.", source: "#" },
      { text: "• Bitcoin struggles with heightened volatility as US tariffs and Fed policy fuel market uncertainty.", source: "#" },
      { text: "• Hong Kong confirms Bitcoin and Ether can be used to secure wealth for investment visa.", source: "#" }
    ]
  }
];

export default function HijauDashboard() {
  console.log("Rendering HijauDashboard Component");
  const [selectedPeriod, setSelectedPeriod] = useState("7days");

  return (
    <>
    {/* top part */}

      <header>
        <div className="header-content">
          <div className="logo">Hijau</div>
            <button className="menu-button" aria-label="Open menu" onClick={() => console.log("Menu button clicked")}>
            <span className="menu-icon">&hellip;</span>
            </button>
        </div>
      </header>
      <hr/>

    {/* in today's hijau */}

      <div className="container-1">
        <h2 className="subtitle">In today's Hijau</h2>

      </div>

    {/* sentiment part */}

      <div className="container">
        <h2 className="subtitle">Sustainability Sentiment Analysis</h2>
        <p className="description">This graph visualizes overall sentiment trends on sustainability topics</p>

        <div className="card-container">
          <div className="card">
            <h3>Fear & Greed Index</h3>
            <p>Current Score: <span className="highlight">58 (Neutral)</span></p>
          </div>
          <div className="card">
            <h3>Historical Values</h3>
            <ul>
              <li>Yesterday: <span className="highlight">55 (Neutral)</span></li>
              <li>Last Week: <span className="highlight">50 (Neutral)</span></li>
              <li>Last Month: <span className="highlight">40 (Fearful)</span></li>
            </ul>
          </div>
          <div className="card">
            <h3>Next Updates</h3>
            <p>Hourly, 7 hours, 3 minutes</p>
          </div>
        </div>

        <div className="chart-section">
          <p>Select Time Period:</p>
          <div className="button-group">
            {['7days', '1month', '3months', '1year', 'max'].map(period => (
              <button key={period} className={selectedPeriod === period ? "button active" : "button"} onClick={() => setSelectedPeriod(period)}>
                {period}
              </button>
            ))}
          </div>

          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={mockData}>
                <XAxis dataKey="date" stroke="#8884d8" />
                <YAxis stroke="#8884d8" />
                <Tooltip />
                <Line type="monotone" dataKey="index" stroke="#82ca9d" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* news part */}
      <div className="news-section">
        {newsData.map((news, index) => (
          <div className="news-container" key={index}>
            <div className="news-header">
              <h3 className="news-title">What's happening in {news.category}</h3>
              <p className="news-date">{news.date}</p>
            </div>
            <div className="news-content">
              <ul>
                {news.articles.map((article, idx) => (
                  <li key={idx}>
                    {article.text} <a href={article.source} target="_blank" rel="noopener noreferrer">(source)</a>
                  </li>
                ))}
              </ul>
              <button className="see-all">See all</button>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
