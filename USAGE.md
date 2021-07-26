Usage
=====

**Endpoints**

# Completion Status
`GET /api/ibl/completion/status/course/<course_id>`

## Params
**Positional**
* `course_id`

**Query params**
* `username` (optional)

### Notes
* If username is blank, it will retrieve information for the requesting user.

* If username is specified, the request must be made by a staff/superuser.

### Examples
```
/api/ibl/completion/status/course/course-v1:edX+DemoX+Demo_Course

/api/ibl/completion/status/course/course-v1:edX+DemoX+Demo_Course?username=student
```


## Return
* `started`: Whether the course was started
* `completed`: Whether the course was completed
* `completion_percentage`: Course completion percentage
* `resume_block_url`: edX "resume" URL
* `course`: Course ID
* `total_units`: Total units _visible to the user_ in the course
* `completed_units`: Completed units according to BlockCompletion



### Example
```
{
    "started": true,
    "completed": false,
    "completion_percentage": 5.13,
    "resume_block_url": "https://edx.example.com/courses/course-v1:edX+DemoX+Demo_Course/jump_to/block-v1:edX+DemoX+Demo_Course+type@html+block@55cbc99f262443d886a25cf84594eafb",
    "course": "course-v1:edX+DemoX+Demo_Course",
    "total_units": 39,
    "completed_units": 2
}
```


# Certificate Status
`GET /api/ibl/completion/status/certificate/<course_id>`

## Params
**Positional**
* `course_id`

**Query params**
* `username` (optional)

### Notes
* If username is blank, it will retrieve information for the requesting user.

* If username is specified, the request must be made by a staff/superuser.

### Examples
```
/api/ibl/completion/status/certificate/course-v1:edX+DemoX+Demo_Course

/api/ibl/completion/status/certificate/course-v1:edX+DemoX+Demo_Course?username=student
```


## Return
* `active`: Whether there is an active certificate
* `status`: Certificate generation status
* `link`: Certificate link

### Examples

_Valid certificate_:
```
{
    "active": true,
    "status": "generated",
    "link": "https://edx.example.com/certificates/1234567"
}
```

_No certificate_:
```
{
    "active": false,
    "status": null,
    "link": null
}
```


# Course Outline
`GET /api/ibl/completion/course_outline/<course_id>`

## Params
**Positional**
* `course_id`

**Query params**
* `username` (optional)

### Notes
* If username is blank, it will retrieve information for the requesting user.

* If username is specified, the request must be made by a staff/superuser.

### Examples
```
/api/ibl/completion/course_outline/course-v1:edX+DemoX+Demo_Course

/api/ibl/completion/course_outline/course-v1:edX+DemoX+Demo_Course?username=student
```


## Return
* `id`: The full block ID (ex: `block-v1:edX+DemoX+Demo_Course+type@html+block@f4a39219742149f781a1dda6f43a623c`)
* `block_id`: The mini block ID (ex: `f4a39219742149f781a1dda6f43a623c`)
* `display_name`: The display name of the block
* `type`: Block type
* `graded`: Whether the section/unit/block is graded
* `resume_block`: Whether the section/unit/block contains, or is, the "resume" block
* `complete`: Whether the section/unit/block has been completed
* `lms_web_url`: Web URL (Use this for linking the block in the context of the entire unit)
* `student_view_url`: XBlock URL (Shows only a single block)
* `children`: A list of objects with the above attributes

### Notes
* The urls returned may use `http` instead of `https`, because of edX's URL construction deficiencies. Might have to change the schema when using this endpoint, though an `https` redirect should happen anyway.

### Example

```javascript
{
  "id": "block-v1:edX+DemoX+Demo_Course+type@course+block@course",
  "block_id": "course",
  "display_name": "Demonstration Course",
  "type": "course",
  "graded": false,
  "resume_block": false,
  "complete": false,
  "student_view_url": "http://edx.example.com/xblock/block-v1:edX+DemoX+Demo_Course+type@course+block@course",
  "lms_web_url": "http://edx.example.com/courses/course-v1:edX+DemoX+Demo_Course/jump_to/block-v1:edX+DemoX+Demo_Course+type@course+block@course",
  "children": [
    {
      "id": "block-v1:edX+DemoX+Demo_Course+type@chapter+block@d8a6192ade314473a78242dfeedfbf5b",
      "block_id": "d8a6192ade314473a78242dfeedfbf5b",
      "display_name": "Introduction"
      "type": "chapter",
      //...
    }
    //...
  ]
}
```
