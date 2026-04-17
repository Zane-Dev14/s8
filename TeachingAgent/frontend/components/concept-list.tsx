"use client";

import { useEffect, useState } from "react";
import { ArrowLeft, BookOpen, CheckCircle2, Circle, Loader2 } from "lucide-react";
import { Card, CardText, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface Concept {
  id: string;
  name: string;
  plain_name: string;
  explanation?: string;
  difficulty: string;
  mastered?: boolean;
}

interface ConceptListProps {
  subjectId: string;
  subjectName: string;
  onSelectConcept: (conceptId: string, conceptName: string) => void;
  onBack: () => void;
}

export function ConceptList({ subjectId, subjectName, onSelectConcept, onBack }: ConceptListProps) {
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/subjects/${subjectId}/concepts`)
      .then((res) => res.json())
      .then((data) => {
        setConcepts(data || []);
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to load concepts");
        setLoading(false);
      });
  }, [subjectId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-orange-50 to-amber-100">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-orange-500 mx-auto mb-4" />
          <p className="text-lg text-gray-600">Loading concepts...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-orange-50 to-amber-100">
        <Card className="p-8 max-w-md">
          <CardTitle className="text-red-600 mb-4">Error</CardTitle>
          <CardText>{error}</CardText>
          <Button onClick={onBack} className="mt-4">Go Back</Button>
        </Card>
      </div>
    );
  }

  const difficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case "beginner":
        return "bg-green-100 text-green-700";
      case "intermediate":
        return "bg-yellow-100 text-yellow-700";
      case "advanced":
        return "bg-red-100 text-red-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-100 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="ghost"
            onClick={onBack}
            className="mb-4 text-orange-600 hover:text-orange-700"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Subjects
          </Button>
          <h1 className="text-4xl font-bold text-orange-600 mb-2">
            {subjectName}
          </h1>
          <p className="text-lg text-gray-700">
            Pick a concept to start your training session!
          </p>
        </div>

        {/* Concept Cards */}
        <div className="space-y-4">
          {concepts.map((concept) => (
            <Card
              key={concept.id}
              className="p-6 hover:shadow-lg transition-shadow cursor-pointer border-2 border-orange-200 hover:border-orange-400"
              onClick={() => onSelectConcept(concept.id, concept.plain_name || concept.name)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    {concept.mastered ? (
                      <CheckCircle2 className="w-6 h-6 text-green-500 flex-shrink-0" />
                    ) : (
                      <Circle className="w-6 h-6 text-gray-400 flex-shrink-0" />
                    )}
                    <div>
                      <CardTitle className="text-lg">
                        {concept.plain_name || concept.name}
                      </CardTitle>
                      {concept.explanation && (
                        <CardText className="text-sm text-gray-600 mt-1">
                          {concept.explanation}
                        </CardText>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2 mt-3 ml-9">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${difficultyColor(concept.difficulty)}`}>
                      {concept.difficulty}
                    </span>
                    {concept.mastered && (
                      <span className="px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-medium">
                        ✓ Mastered
                      </span>
                    )}
                  </div>
                </div>
                <Button
                  className="ml-4 bg-orange-500 hover:bg-orange-600"
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectConcept(concept.id, concept.plain_name || concept.name);
                  }}
                >
                  <BookOpen className="w-4 h-4 mr-2" />
                  Learn
                </Button>
              </div>
            </Card>
          ))}
        </div>

        {concepts.length === 0 && (
          <Card className="p-8 text-center">
            <CardTitle className="mb-4">No Concepts Yet</CardTitle>
            <CardText>
              This subject doesn't have any concepts yet. Upload materials to get started!
            </CardText>
          </Card>
        )}
      </div>
    </div>
  );
}

// Made with Bob
