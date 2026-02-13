from django.test import TestCase

# Create your tests here.

# Question:
# 1: What is export policy for furit from India to South Korea? is furit based food product like dried mango and fresh fruit has different regulations?
        sql = """
            WITH query_embedding AS (
                SELECT %s::vector AS qvec
            )
            SELECT kb.id, kb.content, kb.doc_level, kb.metadata,
                kb.embedding <=> q.qvec AS distance
            FROM knowledge_base kb, query_embedding q
            WHERE (kb.effective_date IS NULL OR kb.effective_date <= %s)
            AND kb.embedding <=> q.qvec < %s
            ORDER BY kb.embedding <=> q.qvec
            LIMIT %s
        """
# No relevant information found in the knowledge base. similarity_threshold = 0.35
# similarity_threshold = 0.65
#
    """_I do not have sufficient information in the knowledge base.
The provided context does not mention any specific export policies for fruits or any other food products to South Korea.
Therefore, it cannot be determined whether there are different regulations for dried mangoes and fresh fruits based on the given information.
The context discusses export controls for dual-use, military goods, nuclear-related items, and sensitive technologies, but does not address fruit exports to South Korea.
 To answer this question accurately, one would need additional information regarding South Korean import regulations for such products.
   Based solely on the provided context, it is not possible to determine if there are different regulations for dried mangoes and fresh fruits.
     The context also mentions a 'catch-all' control for items not specifically listed, but this pertains to military and dual-use items rather than food products.
     Thus, the answer remains that the provided context does not offer the necessary information to address the specific query about fruit exports to South Korea.
    """
