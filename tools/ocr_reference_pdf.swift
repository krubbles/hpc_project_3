// Usage: swiftc tools/ocr_reference_pdf.swift -o /tmp/ocr_reference_pdf
//        /tmp/ocr_reference_pdf input.pdf > output.json
import AppKit
import PDFKit
import Vision

struct RecognizedLine: Codable {
    let text: String
    let confidence: Float
}

guard CommandLine.arguments.count == 2,
      let document = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1])) else {
    fatalError("Expected one readable PDF path")
}
var pages: [[RecognizedLine]] = []
for index in 0..<document.pageCount {
    let lines: [RecognizedLine] = try autoreleasepool {
        guard let page = document.page(at: index) else {
            fatalError("Cannot read page \(index + 1)")
        }
        let bounds = page.bounds(for: .mediaBox)
        let size = NSSize(width: 2400, height: 2400 * bounds.height / bounds.width)
        let thumbnail = page.thumbnail(of: size, for: .mediaBox)
        guard let image = thumbnail.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
            fatalError("Cannot render page \(index + 1)")
        }
        let request = VNRecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.recognitionLanguages = ["en-US"]
        request.usesLanguageCorrection = false
        try VNImageRequestHandler(cgImage: image).perform([request])
        return (request.results ?? []).compactMap { observation in
            guard let candidate = observation.topCandidates(1).first else { return nil }
            return RecognizedLine(text: candidate.string, confidence: candidate.confidence)
        }
    }
    pages.append(lines)
    if (index + 1) % 10 == 0 || index + 1 == document.pageCount {
        FileHandle.standardError.write(Data("OCR \(index + 1)/\(document.pageCount) pages\n".utf8))
    }
}
let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
FileHandle.standardOutput.write(try encoder.encode(pages))
