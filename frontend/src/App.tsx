import './App.css'
import { useState } from 'react'
import type { Source, ApiResponse } from "./types"
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

      const data: ApiResponse = await response.json()

      setAnswer(data.answer)
      setSources(data.sources)
    } catch {
      setError("Something went wrong. Please try again.")
    } finally {
      setLoading(false)

    }
  }

  return (
    <div className="app">
      <div className="app-shell">
        <header className="app-header">
          <div className="app-header__mark" aria-hidden="true" />
          <h1 className="app-header__title">Clinical Evidence Assistant</h1>
          <p className="app-header__description">
            A chatbot for answering your questions about clinical evidence from public medical documents.
          </p>
        </header>

        <main>
          <section className="question-section" aria-labelledby="question-heading">
            <h2 id="question-heading" className="visually-hidden">Ask a clinical evidence question</h2>
            <QuestionInput
              question={question}
              setQuestion={setQuestion}
              loading={loading}
              onAsk={handleAsk}
            />
            {loading && (
              <div className="question-progress" aria-hidden="true">
                <span className="question-progress__bar" />
              </div>
            )}
            <p className="question-hint">
              Answers are generated from retrieved passages in public clinical documents.
            </p>
            {error && (
              <p className="error-alert" role="alert">
                {error}
              </p>
            )}
          </section>

          <section className="results-section" aria-live="polite">
            <Answer answer={answer} />
            <Sources sources={sources} />
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
