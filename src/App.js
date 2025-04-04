// export NODE_OPTIONS=--openssl-legacy-provider

import React, { useState, useEffect } from "react";
import "./App.css";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

// Helper: Convert sentiment score (0–1) to label
function getSentimentLabel(score) {
  if (score >= 0.75) return "Greedy";
  if (score >= 0.55) return "Neutral";
  if (score >= 0.3) return "Fearful";
  return "Very Fearful";
}

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

function App() {
  return (
    <div className="app">
      <HijauDashboard />
      <HijauNews />
      <div className="section-divider"></div>
      <HijauSentiment />
      <div className="section-divider"></div>
      <HijauOthers />

    </div>
  );
}

function HijauDashboard() {
  console.log("Rendering HijauDashboard Component");
  const [selectedPeriod, setSelectedPeriod] = useState("7days");

  return (
    <>
      <header>
        <div className="header-content">
          <div className="logo">Hijau</div>
            <button className="menu-button" aria-label="Open menu" onClick={() => console.log("Menu button clicked")}>
            <span className="menu-icon">&hellip;</span>
            </button>
        </div>
      </header>
    <hr/> 
    </>
  );
}

function HijauNews() {
  const today = new Date();
  const formattedDate = today.toLocaleDateString("en-US", { 
    weekday: 'long', 
    month: 'long', 
    day: 'numeric', 
    year: 'numeric' 
  });

  return (
    <main>
      <div className="container-1">
          <h2 className="subtitle">In today's Hijau</h2>
          <span className="news-date">{formattedDate}</span>

        <div className="two-column-layout">
          {/* Left Column - Stacked articles */}
          <div className="left-column">
            <ArticleCard 
              image="/images/hijau_cups.png"
              category="Environment"
              title="23 Things That Aren't Recyclable"
              author="By Chris Baskind"
            />
            
            <ArticleCard 
              image="/images/hijau_wildfire.png"
              category="Environment"
              title="What Is Fire Weather? Definition and Monitoring"
              author="By Tiffany Means"
            />
          </div>
          
          {/* Right Column - Dolphins article */}
          <div className="right-column">
            <ArticleCard 
              image="/images/hijau_dolphins.png"
              category="ANIMALS"
              title="'Superpod' of More Than 2,000 Dolphins Spotted Frolicking off California Coast"
              author="By Cristen Janes"
              timeAgo="1 hour ago"
              featured={true}
            />
          </div>
        </div>  
      </div>
    </main>
  );
}

function ArticleCard({ image, category, title, author, timeAgo, featured }) {
  return (
    <div className={`article-card ${featured ? 'featured' : ''}`}>
      <div className="article-image">
        <img src={image} alt={title} />
      </div>
      <div className="article-content">
        <span className="article-category">{category}</span>
        <span className="article-title">{title}</span>
        <div className="article-meta">
          <span className="article-author">{author}</span>
          {timeAgo && <span className="article-time">{timeAgo}</span>}
        </div>
      </div>
    </div>
  );
}

function HijauSentiment() {
  const [selectedPeriod, setSelectedPeriod] = useState("week");
  const [sentimentScore, setSentimentScore] = useState(null);
  const [sentimentTrend, setSentimentTrend] = useState([]);
  const [topPosts, setTopPosts] = useState([]);
  
  useEffect(() => {
    fetch(`https://hijau-sentiment-analysis-1.onrender.com/sentiment_score?timeframe=${selectedPeriod}`)
      .then(res => res.json())
      .then(data => setSentimentScore(data.sentiment_score));
  
    fetch(`https://hijau-sentiment-analysis-1.onrender.com/sentiment_trend?timeframe=${selectedPeriod}`)
      .then(res => res.json())
      .then(data => setSentimentTrend(data));
  
    fetch(`https://hijau-sentiment-analysis-1.onrender.com/top_reddit_posts?limit=5`)
      .then(res => res.json())
      .then(data => setTopPosts(data));
  }, [selectedPeriod]);

  const sentimentLabel = sentimentScore !== null ? getSentimentLabel(sentimentScore) : "Loading...";
  
  return(
    <div className="container">
        <h2 className="subtitle">Sustainability Sentiment Analysis</h2>
        <p className="description">This graph visualizes overall sentiment trends from Reddit sustainability communities</p>

        <div className="card-container">
          <div className="card">
            <h3>Fear & Greed Index</h3>
            <p>Current Score: <span className="highlight">
            {sentimentScore !== null 
              ? `${Math.round(sentimentScore * 100)} (${sentimentLabel})` 
              : "Loading..."}
              </span></p>
            <p className="source-note">Source: Reddit posts from r/sustainability, r/climate, and r/renewableenergy</p>
          </div>
          <div className="card">
            <h3>Historical Values</h3>
            <ul>
            {/* Placeholder for future historical data */}
            <li>Yesterday: <span className="highlight">Coming Soon</span></li>
            <li>Last Week: <span className="highlight">Coming Soon</span></li>
            <li>Last Month: <span className="highlight">Coming Soon</span></li>
            </ul>
          </div>
          <div className="card">
            <h3>Next Updates</h3>
            <p>Daily at 7:00 AM</p>
          </div>
        </div>

        <div className="chart-section">
          <p>Select Time Period:</p>
          <div className="button-group">
            {['7days', '1month', '3months', '1year', 'max'].map(period => (
              <button key={period} className={selectedPeriod === period ? "button active" : "button"} onClick={() => setSelectedPeriod(period)}>
                {period.charAt(0).toUpperCase() + period.slice(1)}
              </button>
            ))}
          </div>

          <div className="chart-wrapper">
            {sentimentTrend.length === 0 ? (
              <p style={{ textAlign: "center", color: "gray", fontStyle: "italic" }}>
                No data available for this timeframe.
              </p>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={sentimentTrend}>
                  <XAxis dataKey="date" stroke="#8884d8" />
                  <YAxis stroke="#8884d8" />
                  <Tooltip />
                  <Line type="monotone" dataKey="index" stroke="#82ca9d" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        <div className="top-posts-section">
          <h3>Top Reddit Posts</h3>
          <ul>
            {topPosts.map((post, index) => (
              <li key={index}>
                <strong>{post.date}</strong> - Score: {Math.round(post.score * 100)}
                <p>{post.text}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
  );
}

function HijauOthers() {
  return(
    <div className="news-section">
    <h2 className="subtitle">Recent Developments</h2>

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
  );
}

export default App;