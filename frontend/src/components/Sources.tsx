import type { Source } from "../types"

function Sources({ sources } : { sources: Source[]}) {
    return (
        <>
        {sources.map((source, index) => {
            return <div key={index}>
            <p>Document: {source.document}</p>
            <p>Page Number: {source.page_number}</p>
            <p>{source.text}</p>
            </div> 
        })}
        </>
    )  
}

export default Sources