import type { AnswerProps } from "../types"

function Answer({ answer } : AnswerProps) {
    return (
        <>
            <p>{answer}</p>
        </>
    )
}

export default Answer
