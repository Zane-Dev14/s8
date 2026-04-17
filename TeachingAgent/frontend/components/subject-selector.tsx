"use client";

import { useEffect, useState } from "react";
import { BookOpenCheck, ChevronRight, Loader2 } from "lucide-react";
import { Card, CardText, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface Subject {
  id: string;
  name: string;
  description: string;
  concept_count: number;
  mastered_count: number;
}

interface SubjectSelectorProps {
  onSelectSubject: (subjectId: string, subjectName: string) => void;
}

export function SubjectSelector({ onSelectSubject }: SubjectSelectorProps) {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/subjects")
      .then((res) => res.json())
      .then((data) => {
        setSubjects(data);
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to load subjects");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-orange-50 to-amber-100">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-orange-500 mx-auto mb-4" />
          <p className="text-lg text-gray-600">Loading subjects...</p>
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
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-100 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-orange-600 mb-4">
            🥋 Goku Teaching Agent
          </h1>
          <p className="text-xl text-gray-700">
            Alright! Let's power up your knowledge! Pick a subject to start training.
          </p>
        </div>

        {/* Subject Cards */}
        <div className="grid gap-6 md:grid-cols-2">
          {subjects.map((subject) => {
            const progress = subject.concept_count > 0 
              ? Math.round((subject.mastered_count / subject.concept_count) * 100)
              : 0;

            return (
              <Card
                key={subject.id}
                className="p-6 hover:shadow-xl transition-shadow cursor-pointer border-2 border-orange-200 hover:border-orange-400"
                onClick={() => onSelectSubject(subject.id, subject.name)}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <BookOpenCheck className="w-8 h-8 text-orange-500" />
                    <div>
                      <CardTitle className="text-xl">{subject.name}</CardTitle>
                      <CardText className="text-sm text-gray-600 mt-1">
                        {subject.description || "Ready to learn"}
                      </CardText>
                    </div>
                  </div>
                  <ChevronRight className="w-6 h-6 text-orange-400" />
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Progress</span>
                    <span className="font-semibold text-orange-600">{progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-orange-500 h-2 rounded-full transition-all"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                  <div className="flex gap-2 mt-3">
                    <span className="px-2 py-1 bg-orange-100 text-orange-700 rounded text-xs font-medium">
                      {subject.concept_count} concepts
                    </span>
                    <span className="px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-medium">
                      {subject.mastered_count} mastered
                    </span>
                  </div>
                </div>

                <Button
                  className="w-full mt-4 bg-orange-500 hover:bg-orange-600"
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectSubject(subject.id, subject.name);
                  }}
                >
                  Start Training
                </Button>
              </Card>
            );
          })}
        </div>

        {subjects.length === 0 && (
          <Card className="p-8 text-center">
            <CardTitle className="mb-4">No Subjects Yet</CardTitle>
            <CardText>
              Upload your study materials to get started!
            </CardText>
          </Card>
        )}
      </div>
    </div>
  );
}

// Made with Bob
