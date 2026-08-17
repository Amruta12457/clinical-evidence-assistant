import type { Source } from "../types"

function Sources({ sources }: { sources: Source[]}) {
    if (sources.length === 0) {
        return null
    }

    return (
        <section className="sources-section" aria-labelledby="sources-heading">
            <h2 id="sources-heading" className="section-heading">Supporting evidence</h2>
            <p className="sources-intro">Retrieved from the indexed clinical documents.</p>
            <ol className="source-list">
                {sources.map((source, index) => {
                    return (
                        <li key={index} className="source-card">
                            <div className="source-card__meta">
                                <p className="source-meta-item">
                                    <span className="source-meta-label">Document</span>
                                    <span className="source-meta-value">{source.document}</span>
                                </p>
                                <p className="source-meta-item">
                                    <span className="source-meta-label">Page</span>
                                    <span className="source-meta-value">
                                        {source.page_number != null ? source.page_number : "Not specified"}
                                    </span>
                                </p>
                            </div>
                            <p className="source-card__text">{source.text}</p>
                        </li>
                    )
                })}
            </ol>
        </section>
    )
}

export default Sources
