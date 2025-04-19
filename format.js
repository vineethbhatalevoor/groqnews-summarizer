async function summarizeNews() {
  const newsText = document.getElementById("newsInput").value;
  const summaryOutput = document.getElementById("summaryOutput");

  if (!newsText.trim()) {
    summaryOutput.innerHTML = "Please enter some news text.";
    return;
  }

  try {
    const response = await fetch("https://groqnews-summarizer.onrender.com/summarize-text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: newsText, length: 100 }),
    });

    const data = await response.json();
    if (data.summary) {
      summaryOutput.innerHTML = `<strong>Summary:</strong> ${data.summary}`;
    } else {
      summaryOutput.innerHTML = `<strong>Error:</strong> ${data.error}`;
    }
  } catch (error) {
    summaryOutput.innerHTML = "Error fetching summary!";
  }
}