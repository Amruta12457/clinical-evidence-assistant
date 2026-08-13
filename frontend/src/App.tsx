import './App.css'
import { useState } from 'react'
import type { Source } from "./types"
import Sources from "./components/Sources"

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState<Source[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  return (
    <>
      <h1>Clinical Evidence Assistant</h1>
      <p>A chatbot for answering your questions about clinical evidence from public medical documents.</p>
      <input 
        type="text" 
        placeholder="Enter your question..."
        value={question}
        onChange={(event) => {
          setQuestion(event.target.value)
        }}/>
      <button 
        type="button"
        onClick={async () => {
          console.log(question)

          if (question.trim() === "") {
            setError("Please enter a valid question.")
            return
          }

          const payload = {
            question
          }

          setLoading(true)
          setError('')
          setAnswer('')
          setSources([])

          try {
            const response = await fetch("http://localhost:8000/ask", {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(payload)
            })

            if (!response.ok) {
              throw new Error("Request failed.")
            }

            const data = await response.json()

            setAnswer(data.answer)
            setSources(data.sources)
          } catch (err) {
            setError("Something went wrong. Please try again.")
          } finally {
            setLoading(false)

          }
        }}
        disabled={loading}
      >
        {loading ? "Asking..." : "Ask"}
      </button>

      {error && <p>{error}</p>}

      <p>{answer}</p>

      <Sources sources={sources} />
    </>
  )
}

export default App
