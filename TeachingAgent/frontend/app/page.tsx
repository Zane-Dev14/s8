"use client";

import { useState } from "react";
import { SubjectSelector } from "@/components/subject-selector";
import { ConceptList } from "@/components/concept-list";
import { TeachingSession } from "@/components/TeachingSession";

type View = "subjects" | "concepts" | "teaching";

export default function HomePage() {
  const [view, setView] = useState<View>("subjects");
  const [selectedSubject, setSelectedSubject] = useState<{ id: string; name: string } | null>(null);
  const [selectedConcept, setSelectedConcept] = useState<{ id: string; name: string } | null>(null);

  const handleSelectSubject = (subjectId: string, subjectName: string) => {
    setSelectedSubject({ id: subjectId, name: subjectName });
    setView("concepts");
  };

  const handleSelectConcept = (conceptId: string, conceptName: string) => {
    setSelectedConcept({ id: conceptId, name: conceptName });
    setView("teaching");
  };

  const handleBackToSubjects = () => {
    setSelectedSubject(null);
    setSelectedConcept(null);
    setView("subjects");
  };

  const handleBackToConcepts = () => {
    setSelectedConcept(null);
    setView("concepts");
  };

  if (view === "subjects") {
    return <SubjectSelector onSelectSubject={handleSelectSubject} />;
  }

  if (view === "concepts" && selectedSubject) {
    return (
      <ConceptList
        subjectId={selectedSubject.id}
        subjectName={selectedSubject.name}
        onSelectConcept={handleSelectConcept}
        onBack={handleBackToSubjects}
      />
    );
  }

  if (view === "teaching" && selectedConcept) {
    return (
      <TeachingSession
        conceptId={selectedConcept.id}
        conceptName={selectedConcept.name}
        onComplete={handleBackToConcepts}
      />
    );
  }

  return <SubjectSelector onSelectSubject={handleSelectSubject} />;
}

// Made with Bob
