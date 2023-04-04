INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('Korney Devosky', 'profeelucker@gmail.com', 'korney' ,'MOCK'),
  ('Aleksey Smirnov', 'smilovesmirnov@gmail.com', 'smirnov' ,'MOCK');
INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'korney' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )