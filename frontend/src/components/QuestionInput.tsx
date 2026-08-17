import type { QuestionInputProps } from "../types"

function QuestionInput({ question, setQuestion, loading, onAsk } : QuestionInputProps) {
    return (
        <>
            <input 
            type="text" 
            placeholder="Enter your question..."
            value={question}
            onChange={(event) => {
            setQuestion(event.target.value)
            }}/>
            <button 
                type="button"
                onClick={onAsk}
                disabled={loading}
            >
                {loading ? "Asking..." : "Ask"}
            </button>
        </>
    )
}

export default QuestionInput