const API_URL = process.env.API_URL;

interface Subject {
  id: number;
  name: string;
  abbreviation: string;
  semester: 1 | 2;
  course_professor_id?: number | null;
  laboratory_professor_id?: number | null;
  seminar_professor_id?: number | null;
  project_professor_id?: number | null;
}

export interface SubjectWithAssociation {
  id: number;
  name: string;
  abbreviation: string;
  isCourse: boolean;
  isLaboratory: boolean;
  isSeminar: boolean;
  isProject: boolean;
}

export const fetchSubject = async (subjectAbbreviation: string) => {
  const response = await fetch(
    `${API_URL}/subjects/abbreviation/${subjectAbbreviation}`,
    {
      method: "GET",
      cache: "no-store",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  if (!response.ok) return false;
  const subject = await response.json();
  return subject;
};

export const fetchSubjectsByProfessor = async (professorId: number) => {
  const response = await fetch(
    `${API_URL}/subjects/?` +
      new URLSearchParams({
        professor_id: professorId.toString(),
      }),
    {
      method: "GET",
      cache: "no-store",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  if (!response.ok) return false;
  const result = await response.json();

  const professorSubjects: SubjectWithAssociation[] = [];

  if (Array.isArray(result)) {
    result.forEach((subject: Subject) => {
      const subjectInfo: SubjectWithAssociation = {
        id: subject.id,
        name: subject.name,
        abbreviation: subject.abbreviation,
        isCourse: subject.course_professor_id == professorId,
        isLaboratory: subject.laboratory_professor_id == professorId,
        isSeminar: subject.seminar_professor_id == professorId,
        isProject: subject.project_professor_id == professorId,
      };
      professorSubjects.push(subjectInfo);
    });
  } else {
    console.error("Invalid input data: result should be an array.");
  }
  return professorSubjects;
};