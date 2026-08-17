import type { AnswerProps } from "../types"

function Answer({ answer } : AnswerProps) {
    if (!answer) {
        return null
    }
    return (
        <article className="answer-card">
            <h2 className="section-heading">Answer</h2>
            <p className="answer-text">{answer}</p>
        </article>
    )
}

export default Answer
