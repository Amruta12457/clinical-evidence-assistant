import './App.css'
import { useState } from 'react'
import type { Source } from "./types"
import Sources from "./components/Sources"
import QuestionInput from './components/QuestionInput'
import Answer from './components/Answer'

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState<Source[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAsk = async () => {
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
    } catch {
      setError("Something went wrong. Please try again.")
    } finally {
      setLoading(false)

    }
  }

  return (
    <>
      <h1>Clinical Evidence Assistant</h1>
      <p>A chatbot for answering your questions about clinical evidence from public medical documents.</p>

      <QuestionInput
        question={question}
        setQuestion={setQuestion}
        loading={loading}
        onAsk={handleAsk}
      />

      {error && <p>{error}</p>}

      <Answer answer={answer} />

      <Sources sources={sources} />
    </>
  )
}

export default App
