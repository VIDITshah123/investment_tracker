class DocumentClassifier:
    @staticmethod
    def classify(filename_or_title: str) -> str:
        text = filename_or_title.lower()
        if 'annual' in text or 'ar' in text:
            return 'AnnualReport'
        elif 'transcript' in text or 'concall' in text or 'call' in text:
            return 'ConcallTranscript'
        elif 'presentation' in text or 'investor' in text or 'deck' in text:
            return 'InvestorPresentation'
        elif 'result' in text or 'quarter' in text or 'q1' in text or 'q2' in text or 'q3' in text or 'q4' in text:
            return 'QuarterlyResults'
        return 'CorporateAnnouncement'
