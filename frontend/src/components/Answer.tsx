import type { AnswerProps } from "../types"

function Answer({ answer } : AnswerProps) {
    if (!answer) {
        return null
    }
    return (
        <>
            <p>{answer}</p>
        </>
    )
}

export default Answer
