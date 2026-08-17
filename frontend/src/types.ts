// Defining the Source type
 export type Source = {
  document: string
  page_number: number | null
  text: string
}

// Defining QuestionInputProps type
export type QuestionInputProps = {
  question: string
  setQuestion: (value : string) => void
  loading: boolean
  onAsk: () => void
}