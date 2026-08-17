import type { QuestionInputProps } from "../types"

function QuestionInput({ question, setQuestion, loading, onAsk } : QuestionInputProps) {
    return (
        <form
            className="question-form"
            onSubmit={(event) => {
                event.preventDefault()
                onAsk()
            }}
        >
            <label htmlFor="clinical-question" className="visually-hidden">
                Clinical evidence question
            </label>
            <input
                id="clinical-question"
                className="question-input"
                type="text"
                placeholder="Enter a clinical evidence question…"
                value={question}
                onChange={(event) => {
                    setQuestion(event.target.value)
                }}
                disabled={loading}
                autoComplete="off"
            />
            <button
                className="ask-button"
                type="submit"
                disabled={loading}
                aria-busy={loading}
            >
                {loading && <span className="ask-button__spinner" aria-hidden="true" />}
                {loading ? "Asking..." : "Ask"}
            </button>
        </form>
    )
}

export default QuestionInput
